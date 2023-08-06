"""
Test for the crop region
"""
import numpy as np
from peempy.imageproc import CropRegion
import pytest


@pytest.fixture
def t_image():
    array = np.ones((4, 4))
    #array[:, 0] = 0
    array[:, -1] = 0
    #array[0, :] = 0
    array[-1, :] = 0
    return array


def test_crop_region(t_image):
    """
    Test the crop is done correctly
    """

    array = t_image
    crop = CropRegion(((1, 1), (1, 1)), image=array, offset=(0.5, 0.5))
    cropped = crop.get_cropped_image(shift_order=1)
    assert np.all(cropped == np.array([[1, 0.5], [0.5, 0.25]]))

    # This is equivalent to the first case
    crop = CropRegion(((0, 2), (0, 2)), image=array, offset=(1.5, 1.5))
    cropped = crop.get_cropped_image(shift_order=1)
    assert np.all(cropped == np.array([[1, 0.5], [0.5, 0.25]]))

    # Shift give an array full of 1
    crop = CropRegion(((0, 1), (0, 1)), image=array, offset=(0.0, 0.0))
    cropped = crop.get_cropped_image(shift_order=1)
    assert np.all(cropped == 1)

    crop = CropRegion(((1, 0), (1, 0)), image=array, offset=(-1, -1))
    cropped = crop.get_cropped_image(shift_order=1)
    assert np.all(cropped == 1)


def test_crop_corner_prop(t_image):
    """
    Test if the conernes are computed correctly
    """
    crop = CropRegion(((0, 1), (0, 1)), image=t_image, offset=(0.0, 0.0))
    assert crop.corners == (0, 3, 0, 3)
    crop = CropRegion(((0, 1), (0, 1)), image=t_image, offset=(0.5, 0.5))
    assert crop.corners == (0.5, 3.5, 0.5, 3.5)
