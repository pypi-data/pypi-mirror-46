# -*- coding: utf-8 -*-
"""
Created on Fri Jun 30 09:36:45 2017
test with the dataset
@author: Bonan
"""
from peempy.fileproc import get_normalisation, FolderProcesser
from peempy.paths import ppath
import peempy.imageproc as imageproc

import logging
logger = logging.getLogger(__name__)


def main():
    import argparse
    import numpy as np
    parser = argparse.ArgumentParser(
        description="""Apply drift correction to imagesets.
                                 Expect folder in the form of {}_PCOImage.""")
    parser.add_argument("folder",
                        help="ID of the folder to be processed",
                        type=int)
    parser.add_argument("--norm",
                        "-n",
                        help="ID of normalisation image",
                        type=int)
    parser.add_argument("--batch",
                        help="Mode of operation. single or batch",
                        default=0,
                        type=int)
    parser.add_argument("--norm_name",
                        help="Name of normalisation image",
                        default="norm.tif")
    parser.add_argument("--suffix",
                        help="suffix of the new folders",
                        default="drift")
    parser.add_argument("--verbose",
                        "-v",
                        help="Turn on verbose",
                        action="store_true")
    parser.add_argument("--compatible",
                        help="Compatible to old version of Igor script",
                        action="store_true")
    parser.add_argument("--exclude",
                        "-e",
                        help="Exclude a squence of folders",
                        nargs="*")
    parser.add_argument("--save-xmcd",
                        "-s",
                        help="Flag of saving xmcd",
                        action="store_true")
    parser.add_argument("--no-drift-image",
                        "-ni",
                        help="Flag of not saving drifted images",
                        action="store_false")
    args = parser.parse_args()

    if args.verbose:
        imageproc.set_logging(logging.DEBUG)
        logger.setLevel(logging.INFO)

    # Check regions
    if args.batch == 0:
        args.batch = args.folder

    folder_ids = list(range(args.folder, args.batch + 1))

    if args.norm is not None:
        normfolder = ppath.basedir + "{}_UViewImage".format(args.norm)
        norm = get_normalisation(fdname=normfolder, name=args.norm_name)
    else:
        norm = np.array(1)

    # Process the folder ids
    if args.exclude:
        for exc in args.exclude:
            try:
                folder_ids.remove(int(exc))
            except ValueError:
                logger.warning("{} is not in range defined!".format(exc))

    if args.norm in folder_ids:
        logger.warning("Automatically removed normalisation image")
        folder_ids.remove(args.norm)

    processor = FolderProcesser(folder_ids, norm, mask_ratio=0.93)
    processor.save_xmcd = args.save_xmcd
    processor.save_drifted = args.no_drift_image
    processor.adjust_crop()
    print("Crop region saved")
    if args.compatible is True:
        processor.savesuffix = "UViewImage"

    processor.process_all()
