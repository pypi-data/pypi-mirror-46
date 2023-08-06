# -*- coding: utf-8 -*-
"""
Module for image processing inclusing drift correction etc
"""
import logging
import numpy as np
import scipy.ndimage as ndi
import scipy.fftpack
from skimage.feature import register_translation
from skimage.util import crop
from matplotlib.widgets import RectangleSelector
import matplotlib.pyplot as plt
from peempy.videofig import videofig
from peempy.imgstack import ImageStack
logger = logging.getLogger(__name__)

# Logging


def set_logging(level):
    """Set logging level of this module"""
    logger.setLevel(level)
    consoleHandler = logging.StreamHandler()
    consoleHandler.setLevel(logger.level)
    logger.addHandler(consoleHandler)
    return


fft2 = np.fft.fft2
fftshift = scipy.fftpack.fftshift
#ifft2 = pyfftw.interfaces.numpy_fft.ifft2
ifft2 = np.fft.ifft2


def get_image_centre(image, use_int=False):
    """Return the ceter of a image. Result is a tuple of rounded coordinates"""
    x, y = image.shape
    return round((x - 1) / 2), round((y - 1) / 2)


class ImageSeries(ImageStack):
    """Class represent a series of images for PEEM image dataset
    A subclass of ImageStack"""

    def __init__(self, frames, ref=0, type_cast=None):
        """
        Construct a ImageSeries object
        Parameters
        ----------

        frames: list of array
            40,M,M array containing the data

        ref: int
            index of default reference frame
        """
        super().__init__(frames, type_cast=type_cast)
        self.iref = ref
        self.drift_corrected = False
        self.crop_points = [0] * 4
        self.corrected_frames = None  # corrected frames
        self._crop_setting = None  # Overiden crop settings

    def view_drift_region(self):
        """Preview drift correction region"""

        if self.crop_setting is None:
            raise RuntimeError("Cropping for drift region is not defined.")

        cropped = [
            crop(frame, self.crop_setting).copy() for frame in self.frames
        ]
        show_images_series(cropped)

    def view_corrected(self):
        """View corrected frames"""
        if self.drift_corrected is True:
            self._view(self.corrected_frames)
        else:
            print("Image set not drifted")

    def view_frames(self):
        """View frames"""
        self._view(self.frames)

    def drift_correct(self, iref=None, super_sample=4, mode=None):
        """Conduct drift correction.
        Parameters:
        -----------
        iref: int
            index of the reference frames. Default to self.iref

        test: bool
            do a test run and view results
        """
        if iref is None:
            iref = self.iref
        if self.crop_setting is None:
            raise RuntimeError("Cropping for drift region is not defined.")
        dc = DriftCorrector(self.frames,
                            iref,
                            crop_setting=self.crop_setting,
                            super_sample=super_sample)

        self.corrected_frames = dc.correct(mode=mode)
        self.drifts = dc.drifts_from_initial
        self.drift_corrected = True

    def apply_drift(self, drifts, iref=None):
        """Apply drift by manually input drift vectors"""
        if iref is None:
            iref = self.iref
        dc = DriftCorrector(self.frames, self.iref, self.crop_setting)
        dc.drifts = drifts
        dc.apply_drift_corr()
        self.corrected_frames = dc.corrected_frames
        self.drifts = drifts
        self.drift_corrected = True

    def normalise(self, normImage):
        """Normalise each image using normImage"""
        if normImage == 1:
            return
        self.frames = self.frames / normImage * normImage.mean()
        self.frames = self.frames.astype("uint16", copy=False)

    def apply_circle_mask(self, rel_radius, value):
        """Apply a circular ROI to the images. Where mask is False is
        set to the value passed."""
        mask = get_circular_mask(self.frames[0], rel_radius, None)
        self.frames[:, ~mask] = value

    def substract_counts(self, counts):
        """Substract a background."""
        self.frames = self.frames - counts

    def manual_crop(self, use_mean=False):
        """Set up the crop manually.self
        Parameters:
        -----------
        use_mean: bool
            if yes then use the mean frame to select the crop region.
            By default a series of frames is used.
        """
        if use_mean:
            from selector import select
            fig, ax = plt.subplots()
            ax.imshow(self.frames.mean(axis=0))
            select(self.crop_points, ax)
            plt.show()
        else:
            show_images_series(self.frames, poslist=self.crop_points)

    # Use a property for crop_setting
    @property
    def crop_setting(self):
        if self._crop_setting is not None:
            return self._crop_setting
        elif self.crop_points == [0] * 4:
            return ((0, 0), (0, 0))
        else:
            return p2setting(self.crop_points, self.frames[0].shape)

    # Allow crop_setting to be overiden
    @crop_setting.setter
    def crop_setting(self, value):
        self._crop_setting = value

    def _clear_data(self):
        super(ImageSeries, self)._clear_data()
        del self.corrected_frames
        self.corrected_frames = None


class XMCDImageSeries(ImageSeries):
    """Class for raw data of XMCD capture."""
    NCAPTURES = 10  # Number of the captures per setting

    def __init__(self, *args, **kwargs):
        """
        Initialize an image serial for a standard XMCD capture.
        The capture has the order of on-res-plus, off-res-plus,
        on-res-minus, off-res-minus, each have 10 images.
        For memory efficient drift correction, we store the image in the
        order of on-res-plus, on-res-minus, off-res-plus, off-res-minus.
        This way both the on-res part and off-res part can be returned as
        views of the original array
        """
        super(XMCDImageSeries, self).__init__(*args, **kwargs)

        # Reorder the frames
        ncapt = self.NCAPTURES
        res_mask = np.array(([True] * ncapt + [False] * ncapt) * 2, dtype=bool)
        off_mask = np.array(([False] * ncapt + [True] * ncapt) * 2, dtype=bool)
        self.frames = np.concatenate(
            [self.frames[res_mask], self.frames[off_mask]], axis=0)

        # Construct the new 'mask'
        self.res_mask = np.zeros(ncapt * 4, dtype=bool)
        self.off_mask = np.zeros(ncapt * 4, dtype=bool)
        self.res_mask[:ncapt * 2] = True
        self.off_mask[ncapt * 2:] = True
        self._res_mask = res_mask  # Mask for the original order
        self._off_mask = off_mask  # Mask for the original order

        # Save the index array to map the frames to the original order
        indices = list(range(ncapt)) + list(range(ncapt*2, ncapt*3)) \
                  + list(range(ncapt, ncapt*2)) + list(range(ncapt*3, ncapt*4))
        self.orig_index = indices

    @property
    def res_imgs(self):
        """Return on-resonance images"""
        return self.frames[:self.NCAPTURES * 2]

    @property
    def offres_imgs(self):
        """Return off-resonance images"""
        return self.frames[self.NCAPTURES * 2:]

    @property
    def res_imgs_corr(self):
        """Return on-resonance images"""
        if self.corrected_frames is None:
            return
        return self.corrected_frames[self.NCAPTURES * 2:]

    @property
    def offres_imgs_corr(self):
        if self.corrected_frames is None:
            return
        return self.corrected_frames[self.NCAPTURES * 2:]

    def drift_correct(self, refres=19, refoff=10, super_sample=4, mode=None):
        """
        Conduct drift correction for XMCD data sequence.
        Resonanace and off-resonance images are
        drift-corrected independently.
        refres : reference image for resonance series
        refoff : reference image for off-resonance images
        test: if true only previews the correction and not saving results
        """

        if self.crop_setting is None:
            raise RuntimeError("Cropping for drift region is not defined.")

        if len(self.frames) != self.NCAPTURES * 4:
            raise RuntimeError('Expect {} frame but there is only {}'.format(
                self.NCAPTURES * 4, self.frames))

        # Correct resonance images
        res_mask, off_mask = self.res_mask, self.off_mask
        logger.info("Calculating drift of {} images".format(len(self.frames)))
        dc1 = DriftCorrector(self.res_imgs,
                             refres,
                             self.crop_setting,
                             super_sample=super_sample)
        dc2 = DriftCorrector(self.offres_imgs,
                             refoff,
                             self.crop_setting,
                             super_sample=super_sample)
        self.res_dc = dc1
        self.off_dc = dc2
        # Allocate storage space for the result if not using the
        # INPLACE_DRIFT mode, this requires 3X the memory
        res_corr = dc1.correct(mode=mode)
        offres_corr = dc2.correct(mode=mode)
        if not (dc1.INPLACE_DRIFT and dc2.INPLACE_DRIFT):
            self.corrected_frames = np.zeros(self.frames.shape,
                                             dtype=self.frames.dtype)
            self.corrected_frames[res_mask] = res_corr
            self.corrected_frames[off_mask] = offres_corr
        else:
            self.corrected_frames = self.frames

        self.correctors = [dc1, dc2]
        self.drift_corrected = True
        # This is probably unnecessary
        #self.corrected_frames = self.corrected_frames.astype("uint16")
        return self.corrected_frames


class CropRegion(object):
    """
    Class for manipulating setting of crop
    """

    def __init__(self, crop_setting, offset=(0, 0), image=None):
        """
        Initialise a CropRegion object that supports sub-pixel
        crop settings
        """
        self.crop_setting = np.asarray(crop_setting)
        self.offset = np.asarray(offset)
        self.image = image

    @property
    def crop_setting_with_offset(self):
        """
        Generate the crop-setting with offsets
        """
        new_setting = self.crop_setting.copy()
        d = self.offset

        new_setting[0, 0] += d[0]
        new_setting[0, 1] -= d[0]
        new_setting[1, 0] += d[1]
        new_setting[1, 1] -= d[1]
        return new_setting

    @property
    def corners(self):
        """
        Give the corners of the crop reigon, with offsets added

        :returns: a0_start, a0_finish, a1_start, a1_finish
        """
        crop_s = self.crop_setting
        i, j = self.image.shape

        oi, oj = self.offset
        a0_s = crop_s[0, 0]
        a0_f = i - crop_s[0, 1]
        a1_s = crop_s[1, 0]
        a1_f = i - crop_s[1, 1]
        return a0_s + oi, a0_f + oi, a1_s + oj, a1_f + oj

    def plot_region(self, ax=None, draw_image=True, **kwargs):
        """
        Plot the crop frame with the image
        """
        from matplotlib.patches import Rectangle
        if not ax:
            import matplotlib.pyplot as plt
            plt.figure()
            ax = plt.gca()

        if draw_image:
            ax.imshow(self.image)

        corners = self.corners
        # The second axis is x, and the first is y
        xy = (corners[2], corners[0])
        width = corners[3] - corners[2]
        height = corners[1] - corners[0]

        kwargs_ = {"facecolor": "none", "edgecolor": "r"}
        kwargs_.update(kwargs)
        rec = Rectangle(xy, width, height, **kwargs_)
        ax.add_patch(rec)
        return ax

    def get_cropped_image(self, shift_order=3, copy=False):
        """
        Get the cropped image
        """
        # If requesting reference image use self.refimg
        frame = self.image

        d = np.floor(self.offset)  # Integer drifts
        residual = self.offset - d  # Residual of drift

        # Move cropping area accroding to the existing setting of the drift
        # for this frame. If the drift is correct there should be no
        # translation for the cropped image compared to the reference crop
        # This causes the crop-area to "lock" onto the orignial area.

        # Apply calculated sub-pixel drifts to cropped area is needed
        # The `crop` function does not take subpixel range, we get
        # around this by shifting the frame
        if np.any(residual != 0):
            new_setting = np.array(self.crop_setting, dtype="float")
            new_setting[0, 0] += d[0] - 1
            new_setting[0, 1] -= d[0] + 1
            new_setting[1, 0] += d[1] - 1
            new_setting[1, 1] -= d[1] + 1
            crop_tmp = crop(frame, new_setting, copy=copy)
            # Further offset the crop region by shifting the image
            # in the OPPOSITE direction of the residual offset
            crop_tmp = ndi.shift(crop_tmp, -residual, order=shift_order)
            cropped = crop(crop_tmp, ((1, 1), (1, 1)))
        else:
            cropped = crop(frame, self.crop_setting_with_offset, copy=copy)
        return cropped


class DriftCorrector(ImageStack):
    """A class for correcting drift between frames"""

    DEFAULT_DRIFT_MODE = 'one-pass'  # Defult mode of operation
    INPLACE_DRIFT = False

    def __init__(self,
                 frames,
                 ref=0,
                 crop_setting=((0, 0), (0, 0)),
                 super_sample=4):
        """
        Initialise an instance of DriftCorrector

        :pararm frames: list of arrays of frames to be corrected

        :param ref: Index of the reference frame

        :param crop_setting: Setting of crop of axis 0 and aixs 1. 
          See skimages' crop function.

        :param super_sample: Ratio of super sampling during correction.

        We define the drift being *the tranlation to move the image
        back to the reference*.

        Axis orders are numpy standard (Y, X) for images
        """
        super().__init__(frames)
        self.super_sample = super_sample
        self.corrected_frames = None
        self.ref = ref
        self._refimg = None  # Reference image with improved qaulity
        self.crop_setting = crop_setting
        self._flag_drift_calculated = False
        self.drifts = np.zeros((len(self.frames), 2))
        self.drifts_applied = np.zeros((len(self.frames), 2))

        # Storeage for errors
        # See doc of register_translation
        self.phase_diffs = np.zeros(len(self.frames))
        self.errors = np.zeros(len(self.frames))  # See register_translation

    def view_cropped(self, block=False, **kwargs):
        """
        View cropped frames for calculating translations.
        Calls the get_croped_single method with given kwargs
        """
        cpd = np.array(
            [self.get_croped_single(i, **kwargs) for i in range(len(self))])

        show_images_series(cpd, block=block)

    def get_croped_single(self,
                          index,
                          ignore_drift=False,
                          use_corrected=False,
                          copy=False):
        """
        Get a cropped image given by its index.
        This takes acount any drift it has in self.drifts.

        :param index: Index of the frame to be cropped
        :param ignore_drift: Ignore any existin drft
        :param use_corrected: If true will use corrected image.
          e.g to check the quality of drft correction
        """

        # If requesting reference image use self.refimg
        if use_corrected:
            ignore_drift = True
            frame = self.corrected_frames[index]
        else:
            frame = self.frames[index]

        roi = CropRegion(self.crop_setting, image=frame)

        # Do not take the current drift of the frame into account
        if not ignore_drift:
            # Offset the corp region be the negative mount of the drift
            # The drift vector is from the drifted image to the reference
            # Hence applying the negative will move the crop region to
            # centre onto the freature
            roi.offset = -self.drifts[index]
        res = roi.get_cropped_image(copy=copy)
        return res

    def get_mean_cropped(self):
        """
        Note that the image is linkely to be an array of unit16
        hence we need to convert the refernece image to float
        for averaing
        Generate mean of the cropped image.
        This can be used as the reference for iterative drift unit
        things are converged
        """

        refimg = self.get_croped_single(self.ref).astype(np.float64,
                                                         casting='unsafe',
                                                         copy=True)
        for n, i in enumerate(range(self.nimgs)):
            if n == self.ref:
                continue
            img = self.get_croped_single(i)
            refimg += img

        mean = (refimg / self.nimgs)
        mean.astype(self.frames.dtype)
        return mean

    def calc_drifts(self, refimg=None, ref_otf_update=False):
        """
        Compute the drift vectors
        """

        if refimg is None:
            refimg = self.get_croped_single(self.ref)
            indices = range(self.ref + 1, len(self))
        else:
            indices = range(self.ref, len(self))

        # If we update the refernce energy, make sure that it is a copy
        if ref_otf_update is True:
            refimg = refimg.copy()

        dc = 0  # Counter for drift direction
        for i in indices:
            img = self.get_croped_single(i, copy=False)
            # Registor translation takes the current drift into account
            dft, error, phase_diff = register_translation(
                refimg, img, self.super_sample)

            # Drift is a accumulation effect so we update the future frames
            self.drifts[i:] += dft
            self.errors[i] = error
            self.phase_diffs[i] = phase_diff

            # Update the reference by taking weighted average
            # Only if it is requested
            dc += 1
            if ref_otf_update is True:
                img = self.get_croped_single(i)
                refimg = dc / (dc + 1) * refimg + img / (dc + 1)

        indices = reversed(range(self.ref))
        for i in indices:
            img = self.get_croped_single(i)
            # Registor translation takes the current drift into account
            dft, error, phase_diff = register_translation(
                refimg, img, self.super_sample)
            self.drifts[:i + 1] += dft
            self.errors[i] = error
            self.phase_diffs[i] = phase_diff
            dc += 1
            if ref_otf_update is True:
                img = self.get_croped_single(i)
                refimg = dc / (dc + 1) * refimg + img / (dc + 1)

        # Make sure the reference image has drift 0
        self.drifts -= self.drifts[self.ref]

        self._refimg = refimg
        self._flag_drift_calculated = True
        return self.drifts

    def apply_correction(self, inplace=None):
        """
        Apply drifts to the frames.
        Corrected frames are saved in self.corrected_frames
        """
        if inplace is None:
            inplace = self.INPLACE_DRIFT

        drifts = self.drifts
        fm = self.frames
        if inplace is False:
            res = []
            for d, im in zip(drifts, fm):
                res.append(ndi.shift(im, d))

            res = np.array(res)
            self.corrected_frames = res
        else:
            for d, im in zip(drifts, fm):
                # Apply in place
                ndi.shift(im, d, output=im)
            # Dump the drift to the delta array then reset to zero
            # Since the image has been shifted
            self.drifts_applied += self.drifts
            self.drifts[...] = 0
            res = self.frames
            self.corrected_frames = self.frames

        return res

    @property
    def drifts_from_initial(self):
        """Return the correct drift form the initial image"""
        return self.drifts_applied + self.drifts

    apply_drift_corr = apply_correction

    def correct(self, mode=None):
        """Calculate drifts and apply correction.
        Corrected frames are returned.
        """
        if mode is None:
            mode = self.DEFAULT_DRIFT_MODE
        # Do two passes
        if mode != 'iter':
            self.calc_drifts()
            if mode == 'two-pass':
                ref = self.get_mean_cropped()
                self.calc_drifts(refimg=ref)
        elif mode == 'iter':
            self.calc_drift_iter()

        self.apply_correction()
        return self.corrected_frames

    def calc_drift_iter(self, tol=0.5, verbose=True, max_iter=10):
        """
        Iteratively correct unit the change of the drift vector
        dimishes
        """

        def _drift_residual(d1, d2):
            return np.linalg.norm(d1 - d2, axis=-1).max()

        last_drifts = np.ones((self.nimgs, 2))
        count = 1
        refimg = None
        # Compute the drift until it is converged
        while True:
            drifts = self.calc_drifts(refimg=refimg).copy()
            refimg = self._refimg
            residual = _drift_residual(last_drifts, drifts)
            if residual < tol:
                print("# {}/{} residual: {:.3f}, converged".format(
                    count, max_iter, residual))
                break
            if count > max_iter:
                break
            else:
                if verbose:
                    print("# {}/{} residual: {:.3f},"
                          " unconverged".format(count, max_iter, residual))
                last_drifts = drifts
            count += 1
        if verbose:
            print("Correction completed")

    def _clear_data(self):
        super(DriftCorrector, self)._clear_data()
        del self.corrected_frames
        self.corrected_frames = None


def get_circular_mask(image, rel_radius, offset=None):
    """Return a circular mask of the image

    Parameters
    ----------
    image: ndarray
        image to be used

    rel_radius: float
        relative radius of the circule

    offset: ndarray
        offset of the circle

    Returns
    -------
        circular mask, ndarray
    """

    radius = round(image.shape[0] / 2 * rel_radius)
    cx, cy = get_image_centre(image, use_int=True)
    if offset is not None:
        cx += offset[0]
        cy += offset[1]
    nx, ny = image.shape
    x, y = np.ogrid[-cx:nx - cx, -cy:ny - cy]
    mask = x * x + y * y <= radius * radius
    return mask


def show_images_series(frames, update_scale=False, **args):
    """Show a series of frames and allow select of points"""

    vmax, vmin = args.get("vmax"), args.get("vmin")
    frames = np.asarray(frames)

    # This keep reference to the object
    def redraw(f, ax):
        if not redraw.initialised:
            redraw.im = ax.imshow(frames[f],
                                  animated=True,
                                  vmax=vmax,
                                  vmin=vmin)
            redraw.initialised = True
        else:
            d = frames[f]
            redraw.im.set_array(frames[f])
            if update_scale is True:
                redraw.im.set_clim(d.min(), d.max())

    redraw.initialised = False
    videofig(frames.shape[0], redraw, **args)


def load_image_set(path=None, suffix="tif"):
    """Load all images in a folder"""

    import skimage.io as io
    import os
    if path is None:
        path = os.getcwd()
        logger.info("Using current path")
    else:
        logger.info("Using path {}".format(path))

    imfname = []
    for name in os.listdir(path):
        # print(name)
        if suffix in name:
            imfname.append(os.path.join(path, name))
    imfname.sort()
    dataset = []
    nimages = len(imfname)
    for i, name in enumerate(imfname):
        logger.info("Loading file {} of {}".format(i + 1, nimages))
        dataset.append(io.imread(name))
    return np.array(dataset)


def select(poslist, ax=None):
    """Allow selection of a rectangle

    Parameters
    ----------
    poslist: list of 4 numbers
        List of positions to be keep updated. [x1, y1, x2, y2]

    ax: Axes object
        axes object to draw on. If not passed make a new figure with axes
    """

    def line_select_callback(eclick, erelease):
        'eclick and erelease are the press and release events'
        x1, y1 = eclick.xdata, eclick.ydata
        x2, y2 = erelease.xdata, erelease.ydata
        print("(%3.2f, %3.2f) --> (%3.2f, %3.2f)" % (x1, y1, x2, y2))
        print(" The button you used were: %s %s" %
              (eclick.button, erelease.button))
        poslist[0] = x1
        poslist[1] = y1
        poslist[2] = x2
        poslist[3] = y2

    def toggle_selector(event):
        print(' Key pressed.')
        if event.key in ['Q', 'q'] and toggle_selector.RS.active:
            print(' RectangleSelector deactivated.')
            toggle_selector.RS.set_active(False)
        if event.key in ['A', 'a'] and not toggle_selector.RS.active:
            print(' RectangleSelector activated.')
            toggle_selector.RS.set_active(True)

    if ax is None:
        fig, current_ax = plt.subplots()  # make a new plotting range
    else:
        current_ax = ax

    # drawtype is 'box' or 'line' or 'none'
    toggle_selector.RS = RectangleSelector(
        current_ax,
        line_select_callback,
        drawtype='box',
        useblit=True,
        # don't use middle button
        button=[1, 3],
        minspanx=5,
        minspany=5,
        spancoords='pixels',
        interactive=True)
    plt.connect('key_press_event', toggle_selector)


def xmcd4_from_stack(frames, threshold=0.001):
    """
    Compute xmcd image from a stack of
    L3-plus, Pre-plus, L3-minus, Pre-minus

    Normalised signal is (L3-Pre)/Pre which is then
    passed to the calc_xmcd function

    Returns
    -------

    D image:
        the D image, assymetry of the two polarisations

    I image:
        the I image, sum of two polarisations

    mask:
         ndarray of the mask there True when the sum is LOWER

    """

    frames = np.asarray(frames)
    nimages = frames.shape[0]
    if nimages % 4 != 0:
        raise RuntimeError("Expecting 4N frames but only {} ".format(nimages))

    data = frames.reshape((4, frames.shape[0] // 4) + frames.shape[1:])
    wPlus = data[0].mean(axis=0)
    wOffPlus = data[2].mean(axis=0)
    wMinus = data[1].mean(axis=0)
    wOffMinus = data[3].mean(axis=0)

    # Compute the images to be MCDed
    np.seterr(divide="ignore", invalid="ignore")
    wPlus /= wOffPlus
    wMinus /= wOffMinus
    wPlus -= 1
    wMinus -= 1
    fix_invalid(wPlus)
    fix_invalid(wMinus)
    np.seterr(divide="warn", invalid="warn")
    xmcd, xmcd_sum, mask = calc_xmcd(wPlus, wMinus, threshold)
    return xmcd, xmcd_sum, mask


def calc_xmcd(plus, minus, threshold=0.001):
    """Compute XMCD image given plus and minus image and a threshold

    Returns
    -------

    D image:
        the D image, assymetry of the two polarisations

    I image:
        the I image, sum of two polarisations

    mask:
         ndarray of the mask there True when the sum is LOWER
    than the threshold

    """

    stack = np.stack((plus, minus))
    mask = None

    # select only the region above threshold
    # Make everything positive (from the original script)
    stack = abs(stack) + (stack == 0).astype(np.int) * 1e-5
    xmcd_sum = stack.sum(axis=0)
    mask = xmcd_sum < threshold

    # This essentially set where sum is lower than zero to aproximately 0
    # meanwhile aboiding zero divisions

    signal = (stack[0] - stack[1]) / (xmcd_sum + mask.astype(np.int) * 1e10)

    return signal, xmcd_sum, mask


def fix_invalid(array):
    """Replace invalid values e.g nan and inf with zero"""
    array[~np.isfinite(array)] = 0
    return array


def p2setting(cpoints, imshape):
    """
    Compute cropt setting from points

    Parameters:
    cpoints: sequence (y1,x1,y2,x2)
        Points defining an rectangle

    imshape: (2,) tuple
        shape of the image
    """
    if cpoints is None:
        return
    else:
        poslist = np.asarray(cpoints)
        nx, ny = imshape
        ys = poslist[[0, 2]]
        xs = poslist[[1, 3]]
        x1 = xs.min()
        x2 = nx - xs.max()
        y1 = ys.min()
        y2 = ny - ys.max()
        return ((x1, x2), (y1, y2))
