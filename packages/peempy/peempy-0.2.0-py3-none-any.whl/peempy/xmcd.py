#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module for analysis XMCD images (stacks)
NOTE::
NEED TO STANDARDISE ANGLE MEASUREMENT FRAME
"""
import warnings

import numpy as np
from numpy.linalg import lstsq
from scipy.optimize import curve_fit
from .imgstack import ImageStack
from .aligner import Aligner
from skimage.viewer import CollectionViewer
import skimage.transform as tf
import matplotlib.pyplot as plt
import colorcet

# Angle convantions
# Use standard cartesian coordinates
# theta measured with the equator not the Z axis
# phi from x axis, counterclockwise is positive
# x and y are along their standard direction in the plane
# image is plotted as it is

# Beam angles from N for each FOVs
# these angles are measured with N as the original and CLOCKWISE is positive
beam_angs_N_clockwise = {
    80: 23,
    50: 45,
    40: 54,
    30: 62,
    20: 78,
    15: 93,
    10: 117,
    6: 158,
    None: 0
}
beam_angs = {k: 90 - v for k, v in beam_angs_N_clockwise.items()}
pi = np.pi


class XMCDStack(ImageStack):
    """Class for Stack of XMCD imges for aignment and making vector maps"""
    _attr_save_list = ['angs', 'b_angs']
    _attr_numpy_list = ['angs', 'b_angs']

    def __init__(self, d_imgs, i_imgs, angs, fov):
        """
        Construct an XMCDStack instance given data frames and angles
        Parameters
        ----------
        d_imgs: list of ndarray
            list of D imagees

        i_imgs: list of ndarray
            list of I imagees

        angs: list of numbers
            angles of rotation

        fov: int
            field of views
        """
        d_imgs = np.asarray(d_imgs)
        i_imgs = np.asarray(i_imgs)
        assert d_imgs.shape == i_imgs.shape
        new_frames = np.empty((d_imgs.shape[0] * 2, ) + d_imgs.shape[1:])

        # Store d and i images
        new_frames[0::2] = d_imgs
        new_frames[1::2] = i_imgs
        super().__init__(new_frames)

        # Store angles and beam angles
        self.fov = fov
        self.angs = np.array(angs)
        self.b_angs = np.zeros(self.angs.shape)
        self.b_angs.fill(beam_angs[fov])

        self.mask = np.ones(self.imshape, dtype=bool)
        self.fit_res = None  # Result for fitting (3, M, N) array
        self.fit_residual = None  # Fit residual

    @property
    def d_imgs(self):
        """Difference images"""
        return self.frames[0::2]

    @d_imgs.setter
    def d_imgs(self, value):
        self.frames[0::2] = value

    @property
    def i_imgs(self):
        """Sum images"""
        return self.frames[1::2]

    @i_imgs.setter
    def i_imgs(self, value):
        self.frames[1::2] = value

    @property
    def nimgs(self):
        return len(self.d_imgs)

    def rotate(self, angs):
        """Apply rotation counter clock wise, angs can be an interger or a list"""
        if isinstance(angs, int):
            super().rotate(angs)
        else:
            for i, a in enumerate(angs):
                self.d_imgs[i] = tf.rotate(self.d_imgs[i],
                                           a,
                                           preserve_range=True)
                self.i_imgs[i] = tf.rotate(self.i_imgs[i],
                                           a,
                                           preserve_range=True)
        self.angs += angs  # Change the angles accordingly
        # NOTE beam angle is from N and clockwise is positive
        self.b_angs += angs  # The incident beam_angles should rotate with image

    def derotate(self, iref=0):
        """
        De-rotate frames so that they align with each other rotationwise

        Parameters
        ----------
        iref: int
            index of the reference frame
        """
        angs = self.angs - self.angs[iref]
        self.rotate(-angs)
        self.angs[:] = 0

    def get_aligners(self):
        """Return an aligner object for alignment of frames"""
        self.ai = Aligner(self.i_imgs, grid=2)
        self.ad = Aligner(self.d_imgs, grid=2)
        return self.ad, self.ai

    def apply_alignment(self, ttype="projective", use_only_i=True):
        """Apply alignment from the aligners
        ttype:
            Transform to be applied

        index:
            indices to be aligned

        use_only_i:
            Use only the cpoints from i images
        """
        self.ai.align(ttype)
        if use_only_i:
            self.ad.cpoints = self.ai.cpoints
        self.ad.align(ttype)
        self.frames[0::2] = self.ad.res
        self.frames[1::2] = self.ai.res

    def threshold_i(self, threshold, update=False):
        """Use intensity of images as threshold to update the mask"""
        mask = np.ones(self.imshape, dtype=bool)
        for img in self.i_imgs:
            thres_mask = img > threshold
            mask = thres_mask & mask
        if update is True:
            self.mask = mask
        return mask

    # NOT IN USE?
    def prob(self, x, y, grazing=16, ax=None):
        """A probe for intensity to D images at position x,y"""
        x, y = y, x
        d_sig = self.d_imgs[:, x, y]
        fit = self.fit_res[:, x, y]

        # Initialise coefficient matrix
        # Angles of the K at which the expected intensity is plotted
        plt_angs = np.linspace(-180, 180, 100)
        rangs = plt_angs / 180 * pi
        g = -grazing / 180 * pi  # polar angle of the incident ray

        A = np.vstack([
            np.cos(rangs) * np.cos(g),
            np.sin(rangs) * np.cos(g),
            np.ones(rangs.shape) * np.sin(g)
        ]).T
        model_i = A.dot(fit)

        # Plot
        if ax is None:
            plt.figure()
            ax = plt.subplot(111)
        ax.plot(plt_angs, model_i, "-", label="Fitted signal")
        ax.plot(self.b_angs % 360 - 180, d_sig, "x", label="Measured signal")
        ax.set_title("Fitting at fit_res[{}, {}]".format(x, y))
        ax.set_ylabel("XMCD Asymmetry")
        ax.set_xlabel(r"$\phi_k$ / degrees")
        return plt_angs, model_i, self.b_angs, d_sig, fit

    def view(self):
        """View images"""
        warnings.warn("Using view is ambiguous. Showing I-images.")
        self.view_i()

    def view_i(self):
        """View the I-images"""
        i_imgs_viewer = CollectionViewer(self.i_imgs)
        i_imgs_viewer.show()

    def view_d(self):
        """View the D-Images"""
        d_imgs_viewer = CollectionViewer(self.d_imgs)
        d_imgs_viewer.show()


# OLD METHOD using CURVE fitting
#    def fit_all(self, parallel=None, grid=(100,100)):
#        """Fit a cos wave to the data"""
#        from multiprocessing.pool import Pool
#
#        # Need to change order of axis to allow vectorised resizing
#        if grid is not None:
#            dr = tf.resize(np.moveaxis(self.d_imgs, 0, 2),
#                                   grid, mode="constant",
#                                   preserve_range=True)
#            mr = tf.resize(self.mask,
#                           grid,
#                           mode="constant", preserve_range=True)
#            mr = mr > 0.5
#            to_fit = dr[mr, :].swapaxes(0,1)
#        else:
#            dr = np.moveaxis(self.d_imgs, 0, 2)
#            mr = self.mask
#            to_fit =  dr[mr, :].swapaxes(0,1)
#
#        res_list = []
#        self._res_tmp = res_list
#
#        print("Fitting {} points".format(to_fit.shape))
#        if parallel is not None:
#            p = Pool(parallel)
#            res_list = p.starmap(fit_res, zip([self.angs]*to_fit.shape[-1], to_fit.T))
#        else:
#            for s in to_fit.T:
#                res_list.append(fit_res(self.angs, s))
#
#        # Now construct final result
#        coeff_shape = dr.shape[:2] + (3,)
#        error_shape = coeff_shape
#        self.fit_coeff = np.zeros(coeff_shape)
#        self.fit_error = np.zeros(error_shape)
#        self.fit_residue = np.zeros(dr.shape[:2])
#
#        # unzip the zipped list
#        coeff_list, error_list, residue_list = zip(*res_list)
#        self.fit_coeff[mr, :] = coeff_list
#        self.fit_error[mr, :] = error_list
#        self.fit_coeff = np.moveaxis(self.fit_coeff, 2, 0)
#        self.fit_error = np.moveaxis(self.fit_error, 2, 0)
#        self.fit_residue[mr] = residue_list
#
#        # Modulate the theta
#        self.fit_coeff[1] = self.fit_coeff[1]%360
#
#        # Add resampled to the namespace
#        self.mr = mr
#        self.dr = dr

    def fit_lstsq(self, grazing=16):
        """
        Fit each point using values from the stack using least square method

        Returns:
            (3, P, Q) array of MX, MY and MZ
        """

        res = fit_lstsq_imgs_3D(self.d_imgs, self.b_angs, self.mask, grazing)
        self.fit_res = np.zeros((3, ) + self.imshape)
        self.fit_res[:, self.mask] = res[0]
        if res[1].size != 0:
            self.fit_residual = np.zeros(self.imshape)
            self.fit_residual[self.mask] = res[1]

    def fit_lstsq_2D(self, indices=None):
        """Use 2D fitting. Assuming magnetisation is completely in plane"""
        if indices is None:
            indices = slice(None)
        fit_frames = self.d_imgs[indices]
        res = fit_lstsq_imgs_2D(fit_frames, self.b_angs[indices], self.mask)
        self.fit_res = np.zeros((3, ) + self.imshape)
        self.fit_res[:2, self.mask] = res[0]
        if res[1].size != 0:
            self.fit_residual = np.zeros(self.imshape)
            self.fit_residual[self.mask] = res[1]

    @property
    def fit_res_sph(self):
        """Fitting result in polar angle"""
        if self.fit_res is None:
            raise RuntimeError("Please run least square fitting first")
        else:
            # Use the fitted x and y to get the angle
            # Note that the frame of pixel position is de-coupled from the
            # frame of fitting x, y, z. No need to switch corrdinates here
            # previous angles are reflected with respect to (-1, 1) vector
            sph_img = np.zeros(self.fit_res.shape)
            angs = cart2sph(self.fit_res[:, self.mask])
            sph_img[:, self.mask] = angs
        return sph_img

    @property
    def fit_in_mags(self):
        """In plane magnitude from fitted results"""
        if self.fit_res is None:
            raise RuntimeError("No fitting has been done")
        else:
            return np.hypot(self.fit_res[0], self.fit_res[1])

    @property
    def fit_mags(self):
        """Magnitude of 3D magnetisation vector"""

        if self.fit_res is None:
            return
        else:
            return np.sqrt(np.sum(self.fit_res**2, axis=0))

    def filter_angs(self, angs):
        """Construct new XMCDStack object using desired angles"""

        mask = np.in1d(self.angs, angs)
        new_d = self.d_imgs[mask]
        new_i = self.i_imgs[mask]
        new_stack = XMCDStack(new_d, new_i, angs, fov=self.fov)
        new_stack.b_angs = self.b_angs[mask]
        new_stack.mask = self.mask
        return new_stack

    def show_fit(self, coord):
        """Display fit at a certain point

        Parameters
        ----------
        coord
            tuple of x and y coords"""
        x_data = self.angs
        x = np.linspace(x_data[0], x_data[-1], 100)
        y = cos_curve(x, *self.fit_coeff[:, coord[1], coord[0]])
        y_data = self.d_imgs[:, coord[1], coord[0]]

        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(x, y, '-', label="Fit")
        ax.plot(x_data, y_data, 'x', label="Data")
        ax.legend()
        fig.show()

    def polar_hist(self,
                   cmap="cyclic_mrybm_35_75_c68",
                   bins=360,
                   weighted_by="none"):
        """Polar histogram. Respect the mask defined"""
        from matplotlib.collections import LineCollection

        if isinstance(cmap, str):
            cmap = colorcet.cm[cmap]

        # Calculate histogram
        # The in-plane magnetude is weighted during calculation
        if weighted_by == "none" or weighted_by is None:
            w = np.ones(self.fit_res_sph[0].shape)
        elif weighted_by == "inmags":
            w = self.fit_in_mags
        elif weighted_by == "mags":
            w = self.fit_mags
        else:
            raise RuntimeError("Invalid weighting {}".format(weighted_by))
        value, bin_edges = np.histogram(self.fit_res_sph[0, self.mask],
                                        bins=bins,
                                        weights=w[self.mask])
        phi = bin_edges[:-1]
        width = phi[1] - phi[0]
        phi += width / 2
        fig = plt.figure()

        points = np.array([phi, value]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)
        lc = LineCollection(segments, cmap=cmap, norm=plt.Normalize(0, pi * 2))
        lc.set_array(phi)
        lc.set_linewidth(3)
        ax = fig.add_subplot(111, polar=True)
        # These are necessary as we are using normal spherical coordinates
        #ax.set_theta_direction(-1)
        #ax.set_theta_zero_location('N')

        width = phi[1] - phi[0]
        #plot = ax.scatter(phi, value, c=cmap(phi / (2 * pi)))
        plot = ax.add_collection(lc)

        ax.set_rlim(0, value.max())
        return plot

    def view_angs(self, cmap="cyclic_mrybm_35_75_c68"):
        """Show the in-plane angle plot"""

        print("WARNING: WRONG REPRESENTATION")
        if isinstance(cmap, str):
            cmap = colorcet.cm[cmap]

        data = self.fit_res_sph[0].copy()
        data[~self.mask] = np.nan  # Set where the mask is to be nan

        cmap.set_bad('w', alpha=0)
        if data is None:
            print("Need to fit data first")
        else:
            fig, ax = plt.subplots(1, 1)
            wheel = fig.add_axes([0.8, 0.8, 0.1, 0.1], projection="polar")
            plot_colour_wheel(wheel, cmap=cmap)
            ax.imshow(data, cmap=cmap, vmin=0, vmax=2 * pi)
            ax.set_axis_off()
        return fig

    def view_inmags(self):
        """Show a plot of in plane magnetisations"""

        data = self.fit_in_mags
        data[~self.mask] = 0
        if data is None:
            print("Need to fit data first")
        else:
            fig, ax = plt.subplots(1, 1)
            cax = ax.imshow(data, cmap="gray")
            fig.colorbar(cax)
        return ax


def vec_2imgs(img1, img2, ang1, ang2):
    """
    Calculate in-plane 2 vector giving two images. This assumes zeros OOP
    components.
    """
    ang1 = ang1 / 180 * pi
    ang2 = ang2 / 180 * pi
    norm = np.sin(ang1 - ang2)
    m_x = (-np.sin(ang2) * img1 + np.sin(ang1) * img2) / norm
    m_y = (np.cos(ang2) * img1 + np.cos(ang1) * img2) / norm

    return m_x, m_y


# Utility functions


def cos_curve(x, a, theta, offset):
    """Function to be fitted"""
    return np.cos((x - theta) / 180 * pi) * a + offset


def fit_lst_sq_2D(values, angles):
    """
    Use lst sq method to find the vectors.
    This assume the vectors are purely in plane.

    Ax=b where A is a matrix of coefficients and b is the values.

    Parameters
    ----------
    values : array-like
        list of values to be fitted

    angles : array-like
        list of angles in degrees

    Returns:
    --------
        A list of [(mx, my), residuals, rank, s]. See numpy.linalg.lstsq
    """

    b = values
    rangs = angles / 180 * pi
    A = np.vstack([np.cos(rangs), np.sin(rangs)]).T
    return lstsq(A, b)


def xy2angs(x, y):
    """
    Convert x and y to angles.

    Parameters
    ----------
    x, y :
        array of x and y compoents

    Returns
    -------
    tuple
        (angles, magnitudes) array shape is preserved
    """

    compx = x + 1j * y
    angs = np.angle(compx)

    return angs


def cart2sph(v):
    """
    Take cartesian vectors as input. Return polar coorindates

    :param v:    np array of shape (3,) or (3, N) for one or N vectors

    :return v_sph: A (3,) or (3, N) array of phi, theta and r.
    NOTE theta is measured from the (x, y) plane.
    """
    x, y, z = v
    hxy = np.hypot(x, y)
    r = np.hypot(hxy, z)
    el = np.arctan2(z, hxy)
    az = np.arctan2(y, x)
    return np.array([az, el, r])


def fit_lstsq_imgs_2D(frames, b_angs, mask=None):
    """
    Fit a stack of images
    """
    frames = np.asarray(frames)
    b_angs = np.asarray(b_angs)
    b_angs = 90 - b_angs  # Switch to conventional frame
    rangs = b_angs / 180 * pi
    if mask is None:
        mask = np.ones(frames.shape[-2:], dtype=bool)

    b = frames[:, mask]

    A = np.vstack([np.cos(rangs), np.sin(rangs)]).T

    return lstsq(A, b)


def fit_lstsq_imgs_3D(frames, b_angs, mask=None, grazing=16):
    """
    Fit a stack of K images

    Parameters:
    -----------
    frames: (K, M, N) ndarray
        Frames to be fitted

    b_angs: list of numbers
        beam azimuthal angles in degrees in the standard spherical
    polar coordinate system.

    mask: (M, N) ndarray
        Mask for the frames

    grazing: int, float
        grazing angle of the beam, measured against the x,y plane
    """
    frames = np.asarray(frames)
    b_angs = np.asarray(b_angs)
    # We measure the incident direction using grazing and incident angle
    # The actual wave-vector K is in the direction opposite to it
    # Hence we make g=-grazine and rotate the azimuthal angle by 180 degrees
    rangs = b_angs / 180 * pi + np.pi  # angles in radian
    g = -grazing / 180 * pi
    if mask is None:
        mask = np.ones(frames.shape[-2:], dtype=bool)

    b = frames[:, mask]
    A = np.vstack([
        np.cos(rangs) * np.cos(g),
        np.sin(rangs) * np.cos(g),
        np.ones(rangs.shape) * np.sin(g)
    ]).T

    return lstsq(A, b, rcond=None)


# NOTE need matplotlib <= 2.0
def plot_colour_wheel(ax, cmap='cyclic_mrybm_35_75_c68'):
    """Plot an colour wheel into the axes"""

    import matplotlib as mpl

    if isinstance(cmap, str):
        cmap = colorcet.cm[cmap]

    ax.set_theta_zero_location("N")
    # Negative to allow clockwise to be positive
    # pi to be map 0-1 of the colour map to 0-2pi
    ax._direction = -2 * pi

    norm = mpl.colors.Normalize(0.0, 2 * pi)
    #quant_steps = 2056
    cb = mpl.colorbar.ColorbarBase(ax,
                                   cmap=cmap,
                                   norm=norm,
                                   orientation='horizontal')
    cb.outline.set_visible(False)
    ax.set_axis_off()
    ax.set_rlim([-1, 1])
