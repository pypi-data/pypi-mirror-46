"""Utility tools like data containers and other helpers.

Generally speaking, if a helper functions or class is self-contained and is not
really specific to a more specialized module it is a good candidate for
inclusion here. To make using these helpers easy and cheap this module should
have a low import cost and thus shouldn't use expensive external frameworks.
"""


import warnings
import pprint
from importlib import import_module
from importlib.util import find_spec
from collections.abc import Sequence, Mapping
from functools import lru_cache
from contextlib import contextmanager


__all__ = ["LazyImporter", "LazyMapSequence", "ChainedKeyMap", "expected_warning"]


class LazyImporter:
    """Helper class that delays imports until first access.

    Parameters
    ----------
    imports : dict[str, str]
        A mapping between attribute names and module imports.
    package : str, optional
        Package location from which relative imports are specified. Only
        needed if relative imports are used.
    """

    def __init__(self, imports, package=None):
        self._imports = imports
        self._package = package
        for name, statement in imports.items():
            if name in ("_package", "_imports"):
                raise ValueError(f"name '{name}' is not allowed")
            if find_spec(statement, package) is None:
                # Test if module exists but don't import
                raise ModuleNotFoundError(f"Couldn't find module '{statement}'")

    def __getattribute__(self, name):
        try:
            return object.__getattribute__(self, name)
        except AttributeError:
            _imports = object.__getattribute__(self, "_imports")
            _package = object.__getattribute__(self, "_package")
            if name in _imports.keys():
                value = import_module(_imports[name], _package)
                setattr(self, name, value)
                return value
            else:
                raise


class LazyMapSequence(Sequence):
    """A sequence that applies a function to its items only when accessed.

    Parameters
    ----------
    function : callable
        The function to apply to `items`.
    items : iterable
        An iterable that returns one input argument for `function`.
    cache_size : int, optional
        If a value larger 0 is given, the results of `function` are cached with
        a last recently used cache (LRU) cache of this size.

    Examples
    --------

    >>> files = ["a.txt", "b.txt", "c.txt", "d.txt"]
    >>> for file in files:
    ...     with open(file, "x") as stream:
    ...         stream.write(f"Content of {file}")
    >>> def load(file):
    ...     print(f"Loading {file}")
    ...     with open(file) as stream:
    ...         return stream.read()
    >>> sequence = LazyMapSequence(load, files, cache_size=2)
    >>> len(sequence)
    4
    >>> len(sequence[1:])
    3
    >>> sequence[3]
    Loading c.txt
    "Content of c.txt"
    >>> sequence[3]
    "Content of c.txt"
    """

    def __init__(self, function, items, cache_size=0):
        self.function = function  #: Same as constructor parameter.
        self.items = tuple(items)  #: Same as constructor parameter.

        self._cache_size = cache_size
        if self._cache_size > 0:
            self._get_item = lru_cache(self._cache_size)(self._get_item)

    @property
    def cache_size(self):
        """The size of the LRU cache (int, readonly)."""
        return self._cache_size

    def clear_cache(self):
        """Clear the cache.

        Does nothing if :attr:`~.cache_size` is 0.
        """
        try:
            self._get_item.cache_clear()
        except AttributeError:
            pass

    def __len__(self):
        return len(self.items)

    def __getitem__(self, i_or_slice):
        if isinstance(i_or_slice, slice):
            return self._sliced_subset(i_or_slice)
        else:
            return self._get_item(i_or_slice)

    def _sliced_subset(self, sl):
        # Return new sliced LazyLoadingSequence
        return LazyMapSequence(self.function, self.items[sl], self._cache_size)

    def _get_item(self, i):
        item = self.function(self.items[i])
        return item


class ChainedKeyMap(Mapping):
    """Immutable mapping that implements fancier indexing.

    Parameters
    ----------
    mapping : Mapping
        A mapping to create this class from.
    delimiter : str, optional
        If keys are given as a string this character (sequence) is used to
        split the chained keys.

    Examples
    --------
    >>> ckm = ChainedKeyMap({"a": {"b": 1}, "c": [2, 3, {"d": 4}]})
    >>> ckm["a.b"]
    1
    >>> ckm[("c", 2, "d")]
    4
    >>> ckm[["a.b", ("c", 0)]]
    (1, 2)
    """

    def __init__(self, mapping, delimiter="."):
        self._dict = dict(mapping)

        self.delimiter = delimiter  #: Same as constructor parameter.

    def _get_item(self, keys):
        if isinstance(keys, str):
            keys = keys.split(self.delimiter)
        value = self._dict
        try:
            for key in keys:
                value = value[key]
        except (TypeError, KeyError) as e:
            # Turn Errors into KeyError so that methods of the base class
            # can catch this exception
            raise KeyError(e.args[0])
        if isinstance(value, Mapping):
            value = ChainedKeyMap(value, self.delimiter)
        return value

    def __getitem__(self, keys):
        if isinstance(keys, list):
            return tuple(self[k] for k in keys)
        return self._get_item(keys)

    def __len__(self):
        return self._dict.__len__()

    def __iter__(self):
        return self._dict.__iter__()

    def __repr__(self):
        return f"ChainedKeyMap(\n{str(self)},\ndelimiter='{self.delimiter}')"

    def __str__(self):
        return pprint.pformat(self._dict)


@contextmanager
def expected_warning(message="", category=Warning, module=""):
    """Catch and ignore expected warning.

    Parameters
    ----------
    message : str
        A string compiled to a regular expression that is matched against
        raised warnings to decide whether they are expected.
    category : builtin warning
        A warning category.
    module : str
        A string compiled to a regular expression that is matched against
        the module name of raised warnings to decide whether they are expected.
    """
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", message, category, module)
        yield
