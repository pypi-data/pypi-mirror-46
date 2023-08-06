import pytest

from skimage.data import astronaut
from skimage.color import rgb2gray


@pytest.fixture
def imgs():
    """Fixture for data array"""
    frames = [rgb2gray(astronaut()) for i in range(3)]
    return frames


@pytest.fixture
def img():
    """Fixture for data array"""
    frame = rgb2gray(astronaut())
    return frame


@pytest.fixture
def mock_xmcd():
    from .mock_xmcd import MockXMCD
    return MockXMCD()
