"""
Command for processing XMCD data
"""

import click


@click.command('xmcdlist',
               help='List IDs of captures that have XMCD computed.')
@click.option("--tail", "-t", help="Display only the last N folders", type=int)
@click.pass_context
def xmcdlist(ctx, tail):
    import re

    ppath = ctx.obj['ppath']
    xmcddir = ppath.xmcddir
    iimg_names = sorted(xmcddir.glob('I*.tif'))
    dimg_names = sorted(xmcddir.glob('D*.tif'))
    dnames = set(x.name for x in dimg_names)

    # Search D for each I
    has_d = []
    for img in iimg_names:
        name = img.name
        if name.replace('I', 'D') in dnames:
            has_d.append(True)
        else:
            has_d.append(False)

    imgs_count = len(iimg_names)
    if tail is not None:
        iimg_names = iimg_names[-tail:]
        dimg_names = dimg_names[-tail:]

    # Print out the info
    print(("Displaying {}/{} captures".format(len(iimg_names), imgs_count)))
    print("I Image name     Has D Image")
    print("============     ===========")

    idre = re.compile(r'I_(\d+).tif')
    for iimg, d in zip(iimg_names, has_d):
        has = "X" if d is True else ""
        print(("{:<20}{:<15}".format(idre.match(iimg.name).group(1), has)))


@click.command('xmcdavg', help='Align and average XMCD signals')
@click.argument("folder-id", nargs=-1, required=True)
@click.pass_context
def xmcdavg(ctx, folder_id):
    from .utils import parse_fid
    from peempy.fileproc import XMCDAlign

    ppath = ctx.obj["ppath"]
    fids = []
    for fid in folder_id:
        fids.extend(parse_fid(fid))
    print(folder_id)

    xalign = XMCDAlign(fids, ppath)
    xalign.load_images()
    xalign.select_region()
    xalign.correct_and_save()
