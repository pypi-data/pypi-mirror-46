"""
Module for generating mock XMCD signal
"""

from peempy.imageproc import ImageSeries

from skimage.draw import polygon
from skimage.io import imsave, imshow
import matplotlib.pyplot as plt
import numpy as np


class MockXMCD(ImageSeries):
    def __init__(self, sig=3e5, base_imshape=(512, 512)):
        self.sig = sig
        self.base_imshape = base_imshape
        frames = self.get_test_image_stack().frames
        super(MockXMCD, self).__init__(frames)

    def get_base_image(self):
        """Create the base image with pattern"""
        base_image = np.zeros(self.base_imshape, dtype=np.float)
        trig = np.array([[200, 200], [170, 170], [180, 230]])
        vx, vy = np.mgrid[:200:50, :200:50]
        for x, y in zip(vx.ravel(), vy.ravel()):
            rr, cc = polygon(trig[:, 0] + x, trig[:, 1] + y, self.base_imshape)
            base_image[rr, cc] = self.sig
        return base_image

    def get_test_image_stack(self):
        """Get image stack for testing"""
        image = self.get_base_image()
        frames = np.stack([image] * 40, axis=0)
        # Add backgroun, fake the signal
        frames[20:30] *= 0.9
        frames[10:20] *= -0.1
        frames[30:40] *= -0.1
        ims = ImageSeries(frames)

        drifts = gen_random_drifts()
        self.init_drifts = drifts
        ims.apply_drift(drifts)
        ims.frames = ims.corrected_frames
        add_noise(ims.frames, 1e4)
        # Add the background
        ims.frames += self.sig * 0.5
        ims.apply_circle_mask(0.95, 0)
        return ims


def add_noise(base_image, noise):
    base_image += np.random.random(base_image.shape) * noise


def gen_random_drifts(length=40, v=(0.5, 0.5), rand=5):
    """Introduce a drifts with dominate drifts vector + random noise"""
    dv = np.random.random((length, 2)) * max(v) * rand
    v = dv + v
    return np.cumsum(v, axis=0)


def test_mock_xmcd():
    mxmcd = MockXMCD()
    assert mxmcd.imshape == mxmcd.base_imshape
    assert mxmcd.nimgs == 40
