"""
Created on Wed Jul 12 21:56:35 2017
This module defines ImageStack Class
@author: bonan
"""

import numpy as np
import json
import skimage
import skimage.viewer
import skimage.transform as tf


def get_circular_mask(shape, rel_radius, offset=None):
    """Get a circular mask of the image"""
    nx, ny = shape
    radius = round(shape[0] / 2 * rel_radius)
    cx, cy = round((nx - 1) / 2), round((ny - 1) / 2)
    if offset is not None:
        cx += offset[0]
        cy += offset[1]
    x, y = np.ogrid[-cx:nx - cx, -cy:ny - cy]
    mask = x * x + y * y <= radius * radius
    return mask


class ImageStack:
    """ImageStack basis class"""
    CollectionViewer = skimage.viewer.CollectionViewer
    _attr_numpy_list = []  #list for attribute should be loaded as numpy
    _attr_save_list = []  # list of attribute to be saved in a json

    def __init__(self, frames, type_cast=None):
        """
        Initialise an ImageStack intance by a sequence of frames
        or (N,P,Q) array
        """
        self.frames = np.asarray(frames, dtype=type_cast)
        self.mask = np.ones(self.frames.shape, dtype=bool)
        self._viewer = None

    @property
    def nimgs(self):
        """Number of images stored"""
        return len(self.frames)

    def resize(self, shape, order=1):
        """Resize the entire array"""
        frames = np.moveaxis(self.frames, 0, 2)
        resized = tf.resize(frames,
                            shape,
                            order,
                            mode='reflect',
                            preserve_range=True)
        self._backup()
        self.frames = np.rollaxis(resized, 2)

    def save(self, name):
        """Save array into numpy binary file"""

        print("Saving data to file {}.npy".format(name))
        np.save(name + '.npy', self.frames)
        self._save_attrs(name)

    def load(self, name):
        """"Load frames from numpy binary file"""

        print("Loading data from file {}.npy".format(name))
        self._load_attrs(name)
        self.frames = np.load(name + '.npy')

    @property
    def imshape(self):
        """Shape of each frame"""
        return self.frames[0].shape

    def set_cicular_mask(self, rel, mode="union"):
        """Apply a circular mask to the existing mask
        Parameters
        ----------
        rel: float
            relative radius

        mode: string
            mode of operation. "union" or "replace"
        """
        mask = get_circular_mask(self.imshape, rel)
        if mode == "union":
            self.mask = mask & self.mask
        if mode == "replace":
            self.mask = mask

    @staticmethod
    def _view(data):
        """Show all images using skimage.imshow"""

        viewer = skimage.viewer.CollectionViewer(data)
        viewer.show()

    def view(self):
        """View frames"""

        self._view(self)

    def rotate(self, ang):
        """
        Rotate the stack

        Parameters:
            angs int or list angle of rotations. If a integer is passed
            rotate all frames
        """
        self._backup()
        if isinstance(ang, int):
            frames = np.moveaxis(self.frames, 0, 2)
            self.frames = np.rollaxis(
                tf.rotate(frames, ang, preserve_range=True), 2)
        else:
            for i, a in enumerate(ang):
                self.frames[i] = tf.rotate(self.frames[i],
                                           a,
                                           preserve_range=True)

    def _backup(self):
        """Copy data to self._frames"""
        self._frames = self.frames.copy()

    def _restore(self):
        """Restore from self._frames"""
        self.frames = self._frames

    def __getitem__(self, index):
        """Allow direct slicing"""
        if isinstance(index, tuple) and len(index) == 2:
            return ImageStack(
                self.frames.__getitem__((slice(None, None, None), ) + index))
        else:
            return self.frames.__getitem__(index)

    def __setitem__(self, index, value):
        self.frames.__setitem__(index, value)

    def __len__(self):
        return len(self.frames)

    def __repr__(self):
        string = "<ImageStack at {} with frames: \n".format(id(self))
        string += self.frames.__repr__()
        string += "\n>"
        return string

    def _save_attrs(self, name):
        """Seralize with json. Save np array as lists"""
        json_dict = {}
        for attr in self._attr_save_list:
            value = self.__getattribute__(attr)
            if isinstance(value, np.ndarray):
                value = value.tolist()
            json_dict[attr] = value

        if json_dict:
            with open(name + '.json', "w") as fp:
                json.dump(json_dict, fp)

    def _load_attrs(self, name):
        """Load list as np array"""
        try:
            with open(name + '.json') as fp:
                json_dict = json.load(fp)
        except FileNotFoundError:
            print("No json file found")
            return

        for key, value in json_dict.items():
            if isinstance(value, list) and key in self._attr_numpy_list:
                value = np.array(value)
            self.__setattr__(key, value)

    def _clear_data(self):
        """
        Clear the underlying data
        """
        del self.frames
        del self.mask
        self.frames = None
        self.mask = None
