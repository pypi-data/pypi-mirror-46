#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 21:51:17 2017
this module contains routines for image alignment via control points and
piece wise affine transforms
@author: bonan
"""

import numpy as np
import skimage.io as io
import skimage.transform as tf
import matplotlib.pyplot as plt
from peempy.imgstack import ImageStack
from peempy.graphics import DraggableMarkers


class Aligner(ImageStack):
    """Aligner object for frame alignment via control points"""

    def __init__(self, frames, ref=0, grid=3):
        """Initialise an Aligner object instance"""
        super().__init__(frames)
        self.ref = ref
        self.cpoints = None  # Storage of control points
        self.set_cpts_grid(grid)
        self.res = self.frames.copy()

    @property
    def ncpoitns(self):
        """Control points has shape (N, 2, ncpt, 2)"""
        return self.cpoints.shape[2]

    def save_cpoints(self, name):
        """
        Save defined control points

        Parameters
        ----------
        name str
            name of the file
        """
        print("Saving control points to '{}'".format(name))
        np.save(name, self.cpoints)
        return

    def load_cpoints(self, name):
        """
        Load defined control points

        Parameters
        ----------
        name str
            name of the file
        """
        self.cpoints = np.load(name)
        print("Control points loaded from '{}'".format(name))

    def set_cpts_grid(self, g):
        """Initialise cpts grid"""
        # Calculating padding
        imshape = self.imshape
        xvec = np.linspace(0, imshape[0], g)
        yvec = np.linspace(0, imshape[1], g)
        y, x = np.meshgrid(xvec, yvec)
        x = x.ravel()
        y = y.ravel()
        per_frame = np.stack([x, y]).T
        per_frame = np.stack([per_frame, per_frame])
        self.cpoints = np.stack([per_frame] * self.nimgs, axis=0)

    def set_cpoints_gui(self, i):
        """Set control points for ith frame using GUI"""
        img = self.frames[i]
        ref_points = self.cpoints[i, 0]
        tgt_points = self.cpoints[i, 1]

        fig, axs = plt.subplots(1,
                                2,
                                sharex=True,
                                sharey=True,
                                figsize=(10, 5))
        fig.tight_layout()
        # Plot imges
        axs[0].imshow(self.frames[self.ref], cmap="gray")
        axs[0].set_axis_off()
        axs[1].imshow(img, cmap="gray")
        axs[1].set_axis_off()

        self._ref_dpts = DraggableMarkers(axs[0], ref_points)
        self._tgt_dpts = DraggableMarkers(axs[1], tgt_points)

    def set_size(self, size):
        """Update size of the markers in display"""
        self._ref_dpts.set_size(size)
        self._tgt_dpts.set_size(size)

    def align(self, ttype="projective", index=None, **kwargs):
        """
        Estimate and align from defined control points:

        Avaliable Transforms:
        ---------------------

        'euclidean'         `src, `dst`
        'similarity'        `src, `dst`
        'affine'            `src, `dst`
        'piecewise-affine'  `src, `dst`
        'projective'        `src, `dst`
        'polynomial'        `src, `dst`, `order` (polynomial order,
                                                  default order is 2)
        """

        if index is None:
            index = list(range(self.nimgs))
            index.remove(self.ref)

        self.tforms = {}
        for i in index:
            tform = tf.estimate_transform(ttype, self.cpoints[i, 0],
                                          self.cpoints[i, 1], **kwargs)
            self.tforms[i] = tform
            out = tf.warp(self.frames[i], tform, preserve_range=True)
            self.res[i] = out

        return self.res[index]

    def view_res(self):
        """View the result"""
        if self.res is None:
            raise RuntimeError("Need to align the farmes first")
        self._view(self.res)
