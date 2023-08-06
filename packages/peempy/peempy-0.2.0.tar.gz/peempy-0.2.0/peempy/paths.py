"""
Module for object hold paths of data
PEEM DATA FOLDER SHOULD BE AT: PEEM_DIR 
The standard structure should look like:
PEEM_DIR
|-PCOImage_0000000
|-processing (Can be customized)
  |-xmcd
  |-drift
  |-xmcd_avg

"""

import os
import warnings
from pathlib import Path

# Define alias
path = os.path
pjoin = os.path.join

PEEM_DIR_ENVVAR = "PEEM_DIR"

_WARNING_STRING = """Please set the {} environmental variable.
On bash (linux) this can be done by using command 'export PEEM_DIR=<PATH_TO_DATA>'.
On windows this can be done by command 'set PEEM_DIR=<PATH_TO_DATA>'.""".format(
    PEEM_DIR_ENVVAR)


class PEEMPath:
    """A class for handling information of path of PEEM experiment"""

    # We assume the processing folder is writable
    DEFAULT_PROCESSING_FODLER_NAME = "processing"
    DEFAULT_XMCD_FOLDER_NAME = "xmcd"
    DEFAULT_DRIFT_FOLDER_NAME = "drift"
    DEFAULT_XMCD_AVG_FOLDER_NAME = "xmcd_avg"

    def __init__(self, basedir=None, procdir=None):
        """
        Initialise given the data path e.g the root folder of the
        experiment.

        By default the basedir will be set according to the environmental
        variable. If it does not exist then the current direction will be
        used.
        """
        if basedir is None:
            basedir = os.environ.get(PEEM_DIR_ENVVAR, ".")
            if basedir == ".":
                warnings.warn(_WARNING_STRING)

        self._basedir = Path(basedir)
        self.set_processing_dir(procdir)
        self.set_xmcd_dir()
        self.set_drift_dir()
        self.set_xmcd_avg_dir()

    def set_processing_dir(self, path=None):
        """
        Set the processing directory
        """
        if path is None:
            dtmp = self._basedir / \
                                   self.DEFAULT_PROCESSING_FODLER_NAME
        else:
            dtmp = Path(path)
        self._processing = dtmp

    def set_xmcd_dir(self, path=None):
        """
        Set the directory to svae XMCD data
        """

        if path is None:
            dtmp = self._processing / self.DEFAULT_XMCD_FOLDER_NAME
        else:
            dtmp = Path(path)
        self._xmcd = dtmp

    def set_drift_dir(self, path=None):
        """
        Set the directory to save drift images
        """

        if path is None:
            dtmp = self._processing / self.DEFAULT_DRIFT_FOLDER_NAME
        else:
            dtmp = Path(path)
        self._drift = dtmp

    def set_xmcd_avg_dir(self, path=None):
        """
        Set the diretory to save averaged drift images
        """
        if path is None:
            dtmp = self._processing / self.DEFAULT_XMCD_AVG_FOLDER_NAME
        else:
            dtmp = Path(path)
        self._xmcd_avg = dtmp

    def check_dirs(self):
        """
        Check the existence of directory
        """
        names = ["basedir", "processing", "xmcd", "xmcd_avg", "drift"]
        for nm in names:
            d = self.__dict__["_" + nm]
            etmp = d.exists()
            exist = "exists" if etmp else "does not exists"
            if etmp and not d.is_dir():
                raise RuntimeError("{} is not a directory".format(d))
            print("{}:{} {}".format(nm, d, exist))

    @property
    def basedir(self):
        return self._basedir

    @property
    def procdir(self):
        """Path to the processing folder"""
        return self._processing

    @property
    def driftdir(self):
        """Path of the folder where drifted image sets should be saved"""
        return self._drift

    @property
    def xmcddir(self):
        """Path to the folder where XMCD images should be stored.
        Default is processing/xmcd_out/"""
        return self._xmcd

    @property
    def xmcdavgdir(self):
        """Path of the folder to save the averaged XMCD signals"""
        return self._xmcd_avg


def test_peempath_defaults():
    """
    Basic test of the peempath
    """
    cwd = Path().cwd()
    path = PEEMPath(".")
    assert path.basedir == cwd
    assert path.procdir == cwd / PEEMPath.DEFAULT_PROCESSING_FODLER_NAME
    assert path.xmcddir == path.procdir / PEEMPath.DEFAULT_XMCD_FOLDER_NAME
    assert path.driftdir == path.procdir / PEEMPath.DEFAULT_DRIFT_FOLDER_NAME
    assert path.xmcdavgdir == path.procdir / PEEMPath.DEFAULT_XMCD_AVG_FOLDER_NAME
