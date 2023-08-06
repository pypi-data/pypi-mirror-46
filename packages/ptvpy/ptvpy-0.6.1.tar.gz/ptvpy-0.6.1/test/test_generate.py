"""Test generate module."""


from typing import Generator

import pytest
import pandas as pd
import numpy as np
from numpy.testing import assert_allclose
from scipy.stats import pearsonr

from ptvpy import generate


class Test_add_properties:
    def test_copy(self):
        """Check that a new DataFrame is returned."""
        df = pd.DataFrame({"particle": np.arange(50), "x": np.linspace(0, 10)})
        appended = generate.add_properties(df)
        assert tuple(df.columns) == ("particle", "x")
        assert df.index.size == 50
        assert tuple(appended.columns) == ("particle", "x", "size", "brightness")
        assert appended.index.size == 50

    @pytest.mark.parametrize("size", [(0, 3), (10, 0.01), (2, 0.2)])
    @pytest.mark.parametrize("brightness", [(0, 3), (10, 0.01), (100, 10)])
    def test_correlation(self, size, brightness):
        """Check that brightness and size are always correlated."""
        df = pd.DataFrame({"particle": np.arange(10)})
        df = generate.add_properties(df, size=size, brightness=brightness, seed=42)
        # size and brightness are clipped below 0, don't correlate these
        keep = (0 < df["size"]) & (0 < df["brightness"])
        r, p = pearsonr(df["brightness"][keep], df["size"][keep])
        assert_allclose([r, p], [1, 0], atol=1e-60)


class Test_describe_lines:
    def test_with_wrapping(self):
        frame_count, particle_count = 20, 10
        x_max, y_max = 100, 50
        x_vel, y_vel = 1.5, 20  # Ensure that wrapping happens
        particles = generate.describe_lines(
            frame_count, particle_count, x_max, y_max, x_vel, y_vel, wrap=True, seed=42
        )
        assert tuple(particles.columns) == ("frame", "particle", "x", "y")
        assert len(particles) == frame_count * particle_count
        assert len(particles["frame"].unique()) == frame_count
        assert len(particles["particle"].unique()) == particle_count
        assert particles["x"].values.min() >= 0
        assert particles["x"].values.max() <= x_max
        assert particles["y"].values.min() >= 0
        assert particles["y"].values.max() <= y_max

        for _, particle in particles.groupby("particle"):
            # Assume sort order by frame,
            x_diff = np.diff(particle["x"])
            y_diff = np.diff(particle["y"])
            # correct jumps due to wrapping
            x_diff[x_diff < 0] += x_max
            y_diff[y_diff < 0] += y_max
            # and check particle speed in each direction
            assert_allclose(x_diff, x_vel)
            assert_allclose(y_diff, y_vel)

    def test_without_wrapping(self):
        frame_count, particle_count = 20, 10
        x_max, y_max = 100, 50
        x_vel, y_vel = 1.5, 20  # Ensure that wrapping happens
        particles = generate.describe_lines(
            frame_count, particle_count, x_max, y_max, x_vel, y_vel, wrap=False, seed=42
        )
        assert tuple(particles.columns) == ("frame", "particle", "x", "y")
        assert len(particles) == frame_count * particle_count
        assert len(particles["frame"].unique()) == frame_count
        assert len(particles["particle"].unique()) == particle_count
        assert particles["x"].values.min() >= 0
        assert particles["y"].values.min() >= 0

        for _, particle in particles.groupby("particle"):
            # Assume sort order by frame,
            x_diff = np.diff(particle["x"])
            y_diff = np.diff(particle["y"])
            # and check particle speed in each direction
            assert_allclose(x_diff, x_vel)
            assert_allclose(y_diff, y_vel)


@pytest.mark.parametrize("particle_count", [1, 20, 30])
@pytest.mark.parametrize("angle_vel", [-1, 1, 6, 10])
def test_describe_whirlpool(particle_count, angle_vel):
    frame_count = 100
    radius = 50
    particles = generate.describe_whirlpool(
        frame_count, particle_count, radius, angle_vel=angle_vel, seed=42
    )
    assert tuple(particles.columns) == ("frame", "particle", "x", "y")
    assert len(particles) == frame_count * particle_count
    assert len(particles["frame"].unique()) == frame_count
    assert len(particles["particle"].unique()) == particle_count
    assert particles[["x", "y"]].values.min() >= 0
    assert particles[["x", "y"]].values.max() <= 2 * radius

    for _, particle in particles.groupby("particle"):
        # Assume sort order by frame, move whirlpool origin to (0, 0)
        xy = particle[["x", "y"]] - radius

        # Check that a particle doesn't change the radius inside the whirlpool
        rho = np.linalg.norm(xy, axis=1)
        assert_allclose(rho, rho[0])

        # Calculate angular step between frames
        step = np.diff(np.arctan2(xy["y"], xy["x"]))
        # Correct jumps between quadrant II (-pi/2) and III (pi/2) with modulo,
        # in Python result has same sign as divisor, to get correct step
        # we need a negative divisor for negative angular velocity
        step %= np.pi * np.sign(angle_vel)
        # and check results (comparing absolute value is only meaningful for
        # angular velocities smaller pi)
        assert_allclose(step, step[0])
        assert np.all(np.abs(step) < np.abs(angle_vel))
        assert np.all(np.sign(step) == np.sign(angle_vel))


@pytest.mark.parametrize("shape", [(100,), (20, 20), (10, 10, 10)])
@pytest.mark.parametrize("mu", [0, -1, 10, 1.5])
@pytest.mark.parametrize("variance", [1])
@pytest.mark.parametrize("seed", [None, 42])
def test_white_noise(shape, mu, variance, seed):
    """Basic tests for the golden path and of the output."""
    frames = generate.white_noise(shape, mu, variance, seed)
    assert isinstance(frames, Generator)
    for i, frame in enumerate(frames):
        if i > 10:
            break  # generator is endless, so we need to break here
        assert frame.shape == shape
        # Roughly compare value distibution at 1 * variance
        assert np.sum(mu + variance < frame) < np.sum(frame < mu + variance)
        assert np.sum(mu - variance < frame) > np.sum(frame < mu - variance)
        # and 0.5 variance
        assert np.sum(mu + 0.5 * variance < frame) < np.sum(frame < mu + 0.5 * variance)
        assert np.sum(mu - 0.5 * variance < frame) > np.sum(frame < mu - 0.5 * variance)
