"""
Test for ImageStack class
"""
import pytest
from skimage.data import astronaut
from skimage.color import rgb2gray
import numpy as np
from scipy.ndimage import shift

from peempy.imgstack import ImageStack
from peempy.imageproc import DriftCorrector, ImageSeries, XMCDImageSeries
from peempy.xmcd import XMCDStack


@pytest.fixture
def drift_imgs():
    """Fixture for drifted images"""
    nimages = 5  # Number of images
    frames = [rgb2gray(astronaut()) for i in range(nimages)]
    # Generate random drift
    drift = np.array([np.random.random(2) * 20 for i in range(nimages)])
    drift -= drift[0]
    drift = np.cumsum(drift, axis=0)  # Random displacments
    dataset = np.zeros((len(frames), ) + frames[0].shape)
    for i in range(nimages):
        shift(frames[i], shift=drift[i], output=dataset[i])
    return dataset, drift


@pytest.mark.parametrize("super_sample", [2, 4])
def test_corrector(drift_imgs, super_sample):

    data, init_disp = drift_imgs[0], drift_imgs[1]
    corrector = DriftCorrector(data,
                               crop_setting=((100, 100), (100, 100)),
                               super_sample=super_sample)
    corrector.correct()
    diff = corrector.drifts_from_initial + init_disp
    assert diff.max() < 2 / corrector.super_sample


@pytest.mark.parametrize("super_sample", [2, 4])
def test_corrector_two_pass(drift_imgs, super_sample):

    data, init_disp = drift_imgs[0], drift_imgs[1]
    corrector = DriftCorrector(data,
                               crop_setting=((100, 100), (100, 100)),
                               super_sample=super_sample)
    corrector.correct(mode='two-pass')
    diff = corrector.drifts_from_initial + init_disp
    assert diff.max() < 2 / corrector.super_sample


@pytest.mark.parametrize("super_sample", [2, 4, 8])
def test_iter_corrector(drift_imgs, super_sample):

    data, init_disp = drift_imgs[0], drift_imgs[1]
    corrector = DriftCorrector(data,
                               crop_setting=((100, 100), (100, 100)),
                               super_sample=super_sample)
    corrector.calc_drift_iter(tol=1 / super_sample)
    diff = corrector.drifts_from_initial + init_disp
    assert diff.max() < 2 / corrector.super_sample


def test_drift_correction(drift_imgs):
    """Test drift_correction"""
    data, init_drift = drift_imgs[0], drift_imgs[1]
    stack = ImageSeries(data)
    stack.crop_setting = ((100, 100), (100, 100))
    stack.drift_correct()
    diff = stack.drifts + init_drift
    assert diff.max() < 0.5, "Difference: {}".format(
        diff)  # Tolorance 1.5 pixels


def test_xmcd_series(mock_xmcd):
    """Test XMCD drift correction on a challenging, noisy dataset"""
    from peempy.imageproc import XMCDImageSeries, xmcd4_from_stack
    xseries = XMCDImageSeries(mock_xmcd.frames.astype(np.uint16))
    xseries.crop_setting = ((150, 150), (150, 150))
    xseries.drift_correct()

    # Computed drift
    resdrift = xseries.correctors[0].drifts_from_initial
    offdrift = xseries.correctors[1].drifts_from_initial

    # Initially applied drift
    init_resdrift = mock_xmcd.init_drifts[xseries._res_mask]
    init_offdrift = mock_xmcd.init_drifts[xseries._off_mask]

    init_resdrift -= init_resdrift[-1]
    init_offdrift -= init_offdrift[10]
    ddrift = np.linalg.norm((init_resdrift + resdrift), axis=-1)
    # The dataset is rather challenging, allow a mean devidation of 3 pixel
    assert ddrift.mean() < 5

    ddrift = np.linalg.norm((init_offdrift + offdrift), axis=-1)
    assert ddrift.mean() < 5

    # Check if this works
    xmcd = xmcd4_from_stack(xseries.corrected_frames)
