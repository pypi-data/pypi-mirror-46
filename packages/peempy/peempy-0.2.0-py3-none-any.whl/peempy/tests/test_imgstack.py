import pytest

import numpy as np

from peempy.imgstack import ImageStack


@pytest.fixture
def stack(request, imgs):
    return ImageStack(imgs)


def test_init(imgs):
    stack = ImageStack(imgs)
    assert np.all(stack.frames == np.asarray(imgs))


def test_rotation(stack):
    old_frames = stack.frames.copy()
    stack.rotate(90)
    stack.rotate(-90)
    assert np.all((old_frames - stack.frames) <= 1e-5)
