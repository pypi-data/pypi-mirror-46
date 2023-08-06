"""
Command line module for batch processing
"""
import click

import logging
logger = logging.getLogger(__name__)

from .utils import parse_fid


@click.command("drift", help="Perform batch drift operation. ")
@click.argument("folder-id", nargs=1, required=True)
@click.option("--verbose", "-v", help="Increase the verbosity", count=True)
@click.option("--norm-id", "-norm", help="ID of the normalisation image")
@click.option("--save-xmcd/--no-save-xmcd",
              help="Save XMCD image or not, default: true",
              default=True)
@click.option("--save-drift/--no-save-drift",
              help="Save drifted images or not, default: true",
              default=True)
@click.option("--drift-folder-name",
              help="Name of the folder used for saving the drift images",
              default="drift")
@click.option("--xmcd-folder-name",
              help="Name of the folder used for saving the drift images",
              default="xmcd")
@click.option("--folder-suffix",
              help="Suffix of the image folder name <ID>_<SUFFIX>",
              default="PCOImage")
@click.option("--norm-name",
              help="Name of the normalization image inside the folder",
              default="norm.tif")
@click.option("--nprocs",
              "-np",
              help="Number of processes in parallel",
              type=int,
              default=0)
@click.pass_context
def drift(ctx, folder_id, verbose, norm_id, save_xmcd, save_drift,
          drift_folder_name, xmcd_folder_name, folder_suffix, norm_name,
          nprocs):
    """
    Perform drift correction and save XMCD signals
    """
    from peempy.fileproc import get_normalisation, FolderProcesser
    from peempy.paths import PEEMPath
    import peempy.imageproc as imageproc
    import os

    if verbose:
        imageproc.set_logging(logging.DEBUG)
        logger.setLevel(logging.INFO)

    ppath = ctx.obj["ppath"]
    if norm_id is not None:
        normfolder = ppath.basedir + "{}_{}".format(norm_id, folder_suffix)
        norm = get_normalisation(fdname=normfolder, name=norm_name)
    else:
        import numpy as np
        norm = np.array(1)

    folder_id = parse_fid(folder_id)
    print(folder_id)
    folder_id = filter_fids(ppath, folder_id, folder_suffix)
    print(folder_id)
    if verbose:
        click.echo("Processing {} folder, starting from {}".format(
            len(folder_id), folder_id[0]))

    processor = FolderProcesser(folder_id,
                                norm,
                                mask_ratio=0.93,
                                peempath=ppath)

    processor.DATASUFFIX = folder_suffix
    processor.SAVESUFFIX = folder_suffix
    processor.nprocs = nprocs
    processor.save_xmcd = save_xmcd
    processor.save_drifted = save_drift

    processor.adjust_crop()
    processor.process_all()


def filter_fids(ppath, ids, suffix, fcount=40):
    """
    Scan a list of folder ids, exclude those not valid
    """
    res = []
    for folder_id in ids:

        fpath = ppath.basedir / "{}_{}".format(folder_id, suffix)
        if not fpath.is_dir():
            continue
        # check the number of tif files
        print(fpath)
        tifs = list(fpath.glob('*.tif'))
        if len(tifs) != fcount:
            continue
        else:
            res.append(folder_id)
    return res
