import pytest
from ..xmcd import fit_lstsq_imgs_3D
from ..utils import r2d, d2r
import numpy as np


def eq_zero(x):
    return abs(x - 0) < 1e-14


@pytest.fixture
def img_oop():
    """
    Image stack with one pixel and the magnetisation should be in -z direction
    """
    stack = np.array([[[1]]] * 5)
    b_angs = np.array([0, 30, 60, 90, 120])
    return stack, b_angs


@pytest.fixture
def img_ip():
    """
    Image stack with one pixel and the magnetisation should be in (1, 1, 0) direction
    """
    b_angs = np.array([0, 30, 60, 90, 120])

    def gen_ip_img(azi_ang=45):
        intensity = np.cos(d2r(b_angs - azi_ang))
        stack = np.zeros((5, 1, 1))
        stack[:, 0, 0] = intensity
        return stack, b_angs

    return gen_ip_img


def test_lstsq_fit_oop(img_oop):
    stack, b_angs = img_oop
    fit_res = fit_lstsq_imgs_3D(stack, b_angs, grazing=45)[0]
    assert np.all(eq_zero(fit_res[0]))
    assert np.all(eq_zero(fit_res[1]))
    assert np.all(fit_res[2] < 0)


@pytest.mark.parametrize("azi_ang", [45, -30, 120, -135])
def test_lstsq_fit_ip(img_ip, azi_ang):
    stack, b_angs = img_ip(azi_ang)
    fit_res = fit_lstsq_imgs_3D(stack, b_angs, grazing=45)[0]
    if azi_ang % 180 == 45:
        assert np.all(abs(fit_res[0] - fit_res[1]) < 1e-14)
    assert np.all(eq_zero(fit_res[2]))
