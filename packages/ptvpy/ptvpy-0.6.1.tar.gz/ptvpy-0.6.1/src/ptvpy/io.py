"""Tools to manage data on disk."""


import glob
import hashlib
import re

import numpy as np
import pandas as pd
import imageio
import h5py

from .process import mean_frame
from .utils import LazyMapSequence


__all__ = ["HdfFile", "FrameLoader", "hash_files", "hash_arrays"]


class HdfFile(h5py.File):
    """Simple wrapper to handle IO for more complex types.

    This class makes it possible to round-trip pandas.DataFrames through the
    two methods :meth:`save_df` and :meth:`load_df`.

    Notes
    -----
    Because the implementation was kept very simple, it is likely that storing
    DataFrames with more exotic or complex dtypes (especially "object") will
    fail. However numeric dtypes should work. While the DataFrame support is
    not as thorough as the one in panda's HDFStore, this class exposes the full
    range of h5py's API and allows attribute access and storage of more complex
    data. Furthermore 'pytables' can be skipped as a dependency.

    The way this wrapper stores DataFrames is by creating a new group at a
    desired `path`. This group then contains a dataset for each column in the
    DataFrame.
    """

    def save_df(self, path, df, overwrite=True, **kwargs):
        """Store a pandas DataFrame.

        .. warning::

           - Doesn't preserve the index of a DataFrame. If you want to save the
             index convert it into a column beforehand.
           - Doesn't preserve column order.
           - Column names must be strings.
           - Saving DataFrames with non-numeric dtypes may fail.

        .. _create_dataset: http://docs.h5py.org/en/stable/high/group.html#Group.create_dataset

        Parameters
        ----------
        path : str
            Path to store the DataFrame at.
        df : pandas.DataFrame
            The DataFrame to store.
        overwrite : bool, optional
            If False, raises a TypeError if an object already exists at `path`.
            Otherwise an existing object is silently overwritten.
        kwargs : dict
            Additional keyword arguments used to create the dataset for each
            column in `df` (see create_dataset_).
        """
        if overwrite and path in self:
            del self[path]
        group = self.create_group(path)
        for name, series in df.items():
            group.create_dataset(name=name, data=series.values, **kwargs)

    def load_df(self, path):
        """Load a pandas DataFrame.

        Parameters
        ----------
        path : str
            The path to the stored DataFrame.

        Returns
        -------
        df : pandas.DataFrame
            The loaded DataFrame.
        """
        group = self[path]
        df = pd.DataFrame(
            {
                # Load actual content by appending [:], without it creation may be
                # super slow for large DataFrames
                name: group[name][:]
                for name in group.keys()
            }
        )
        return df


class FrameLoader:
    """Helper to load frames without wasting memory and CPU time.

    Parameters
    ----------
    pattern : str
        The path using a glob pattern to match the image files.
    slice_ : slice, optional
        Select a subset of all frames found with `pattern`.

    Notes
    -----
    After calling the method `queue_background_removal` the background will
    be removed upon loading a frame. If the function was provided with a
    file path the background is cached as an intermediate result. If we provide
    the same path again on a new loader we can reuse the result under the
    condition that exactly the same frames are used again. This is checked by
    comparing a hash of the data files specified by `pattern`.

    Examples
    --------
    Most simple way to load TIFF files located inside a directory "data":

    >>> frames = FrameLoader("data/*.tiff").lazy_frame_sequence()

    Load frames but (optionally) remove background, only use first 100 frames
    and load background from "cache.hdf5" if it was already calculated:

    >>> loader = FrameLoader("data/*.tiff", range_=[None, 100])
    >>> loader.queue_background_removal("cache.hdf5")
    >>> frames = loader.lazy_frame_sequence()
    """

    def __init__(self, pattern, slice_=None):
        self.pattern = str(pattern)  #: Same as input argument.
        self.slice_ = slice_  #: Same as input argument.
        #: Boolean flag that is true when the background was loaded from cache
        #: (bool or None).
        self.used_background_cache = None
        self._hash = None
        self._background = None
        self._load_func = imageio.imread

    @property
    def files(self):
        """
        Paths to the files the frames are loaded from (list[str], read-only).
        They are sorted naturally [1]_ and not in alphabetical order.

        .. [1] https://en.wikipedia.org/wiki/Natural_sort_order
        """
        files = sorted(glob.glob(self.pattern), key=_natural_sort_key)
        if self.slice_ is not None:
            files = files[self.slice_]
        return files

    @property
    def hash(self):
        """
        Hexadecimal digits unique to the used data files (str, read-only).
        """
        if self._hash is None:
            self._hash = hash_files(self.files)
        return self._hash

    def lazy_frame_sequence(self):
        """Lazily load frames from the disk.

        Returns
        -------
        frames : LazyMapSequence[ndarray]
            A sequence of frames. Each frame is only loaded from disk when it
            is accessed directly.
        """
        return LazyMapSequence(self._load_func, self.files)

    def load_background(self, cache_path=None):
        """Load (calculate) the average per pixel for all used frames.

        Parameters
        ----------
        cache_path : str, optional
            Path to an HDF5 file that is used to cache the background. If not
            provided or a cache matching the used frames doesn't exist it is
            calculated.

        Returns
        -------
        background : ndarray
            An array matching the frames in shape containing the average per
            pixel for all used frames.
        """
        if self._background is None and cache_path is not None:
            self._load_background_cache(cache_path)
        if self._background is None:
            self._background = mean_frame(self.lazy_frame_sequence())
            self.used_background_cache = False
        if cache_path is not None and not self.used_background_cache:
            self._save_background_cache(cache_path, self._background)
        return self._background

    def queue_background_removal(self, cache_path=None):
        """Automatically remove background when loading a frame.

        After calling this method all loaded frames returned will have their
        background removed.

        Parameters
        ----------
        cache_path : str, optional
            Path to an HDF5 file that is used to cache the background. If not
            provided or a cache matching the used frames doesn't exist it is
            calculated.
        """
        if self._background is None:
            self._background = self.load_background(cache_path)

        def func(path):
            frame = imageio.imread(path)
            frame = frame.astype(np.float64) - self._background
            frame[frame < 0] = 0
            return frame

        self._load_func = func

    def _load_background_cache(self, path):
        try:
            with h5py.File(path, "r") as file:
                if (
                    "background" in file
                    and file["background"].attrs["digest"] == self.hash
                ):
                    # Digest matches -> use cached result
                    self._background = file["background"][...]
                    self.used_background_cache = True
                    return self._background
        except OSError:
            pass
        return None

    def _save_background_cache(self, path, background):
        with h5py.File(path, "a") as file:
            if "background" in file:
                del file["background"]
            # Cache the compressed result with the digest for next use
            file.create_dataset(
                "background", data=background, compression="gzip", compression_opts=8
            )
            file["background"].attrs["digest"] = self.hash
            file["background"].attrs["descr"] = "Average per pixel for all used frames"


def hash_files(paths, *, algorithm=None, buffer_size=2 ** 20):
    """Hash the given `files`.

    Parameters
    ----------
    paths : Iterator[path_like]
        Paths to the files to hash. The order doesn't matter because they are
        sorted before hashing.
    algorithm : _hashlib.HASH, optional
        An object implementing the interface of the algorithms in Python's
        module `hashlib`; namely the methods `update` and `hexdigest`. If not
        provided the algorithm defaults to `hashlib.sha1()`.
    buffer_size : int, optional
        The buffer size in bytes used when hashing files. Changing this
        shouldn't change the computed hash.

    Returns
    -------
    hexdigest : str
        A digest as a string of hexadecimal digits.
    """
    if algorithm is None:
        algorithm = hashlib.sha1()
    for path in sorted(paths):
        with open(path, "rb") as stream:
            while True:
                buffer = stream.read(buffer_size)
                if not buffer:
                    break
                algorithm.update(buffer)
    return algorithm.hexdigest()


def hash_arrays(arrays, *, algorithm=None):
    """Hash the content of arrays.

    Parameters
    ----------
    arrays : Iterable[bytes-like]
        A iterable of objects supporting Python's Buffer Protocol like
        `numpy.ndarray` or `memoryview`.
    algorithm : _hashlib.HASH, optional
        An object implementing the interface of the algorithms in Python's
        module `hashlib`; namely the methods `update` and `hexdigest`. If not
        provided the algorithm defaults to `hashlib.sha1()`.

    Returns
    -------
    hexdigest : str
        A digest as a string of hexadecimal digits.
    """
    if algorithm is None:
        algorithm = hashlib.sha1()
    for obj in arrays:
        algorithm.update(obj)
    return algorithm.hexdigest()


def list_hdf_file(file_or_path):
    """Print objects inside an HDF file.

    Parameters
    ----------
    file_or_path : path_like or h5py.File
        Path to or an open handler to a HDF file.
    """

    def inspect(name, obj):
        if isinstance(obj, h5py.Group):
            print(f"'{name}' (Group)")
        else:
            print(f"'{name}' (Dataset, shape: {obj.shape}, dtype: {obj.dtype})")
        for key, value in obj.attrs.items():
            print(f"    '{key}' (Attribute) : {value} ")

    file = None
    close_after = False
    try:
        if isinstance(file_or_path, h5py.File):
            file = file_or_path
        else:
            close_after = True
            file = h5py.File(file_or_path, "r")
        file.visititems(inspect)

    finally:
        if close_after and file:
            file.close()


def _natural_sort_key(string: str):
    """Transforms strings into tuples that are sorted in natural order [1]_.

    This can be passed to the "key" argument of Python's `sorted` function.

    Examples
    --------
    >>> _natural_sort_key("image_2.png")
    ("image_", 2, ".png")
    >>> _natural_sort_key("image_10.png")
    ("image_", 10, ".png")

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Natural_sort_order
    """
    splitted = re.split(r"(\d+)", string)
    return tuple(int(x) if x.isdigit() else x for x in splitted)
