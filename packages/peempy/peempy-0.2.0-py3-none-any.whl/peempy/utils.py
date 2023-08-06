import numpy as np
import os


def r2d(angs):
    return angs / np.pi * 180


def d2r(angs):
    return angs / 180 * np.pi


def mkdir(dirname):
    """Make dir if not exisit"""
    if not os.path.isdir(dirname) and not os.path.isfile(dirname):
        os.mkdir(dirname)


def normalize_uint8(float_array, perc=3):
    """
    Readjust the range using the percentile
    For generating previews of float data
    return an uint8 array
    """
    lower = np.percentile(float_array.ravel(), perc)
    upper = np.percentile(float_array.ravel(), 100 - perc)
    float_array -= lower
    float_array /= (upper - lower)
    normalized = np.zeros(float_array.shape, dtype=np.uint8)
    normalized = np.clip(float_array, 0, 1)
    normalized *= 255
    return normalized.astype(np.uint8)


def compute_edge(frames, sigma=2.5):
    """
    Compute mean edge image for a stack
    """
    from skimage.feature import canny

    frames = abs(frames) + (frames == 0).astype(np.int) * 1e-5
    edge_mean = np.zeros(frames[0].shape, dtype=np.float)
    for f in frames:
        edge_mean = edge_mean + canny(f, sigma=sigma)

    edge_mean /= len(frames)
    return edge_mean
