"""
Command line module
"""

import click
from .cmd_batch import drift
from .cmd_xmcd import xmcdlist, xmcdavg


@click.group(invoke_without_command=True)
@click.option("--version",
              is_flag=True,
              default=False,
              help="Display the version of PEEMPY")
@click.option("--peem-data-dir",
              "-pd",
              envvar="PEEM_DIR",
              help="The beamline data directory")
@click.option("--work-dir",
              "-wd",
              envvar="PEEM_WORK_DIR",
              help="The base directory to be used for saving processed")
@click.option("--drift-mode",
              "-dm",
              help='Drift correction mode',
              type=click.Choice(['one-pass', 'two-pass', 'iter']))
@click.option("--float-precision",
              "-fp",
              help='Floating point precision when saving XMCD signal',
              type=click.Choice(['single', 'double']))
@click.pass_context
def peemcli(ctx, version, peem_data_dir, float_precision, work_dir,
            drift_mode):
    """
    The command line interface of peempy
    """
    import peempy
    from peempy.paths import PEEMPath

    ppath = PEEMPath(peem_data_dir)
    ppath._procdir = work_dir
    ctx.ensure_object(dict)
    ctx.obj["ppath"] = ppath

    if drift_mode is not None:
        # Overide the default mode
        from peempy.imageproc import DriftCorrector
        DriftCorrector.DEFAULT_DRIFT_MODE = drift_mode

    if float_precision is not None:
        from peempy import fileproc
        import numpy as np
        if float_precision == 'single':
            fileproc.SAVE_DTYPE = np.float32
        elif float_precision == 'double':
            fileproc.SAVE_DTYPE = np.float64

    prompt = ".. exists" if ppath.basedir.is_dir() else ".. does not exists"
    click.echo("DATA directory:{} {}".format(ppath.basedir, prompt))
    prompt = ".. exists" if ppath.procdir.is_dir() else ".. does not exists"
    click.echo("PROCESSING directory:{} {}\n".format(ppath.procdir, prompt))

    if ctx.invoked_subcommand is None:
        if version:
            click.echo("peempy version {}.\nHave a nice day!".format(
                peempy.__version__))
        else:
            click.echo("Please provide a subcommand")

        return


@click.command("datalist", help="Print the avaliable datafolders")
@click.option("--tail", "-t", help="Display only the last N folders", type=int)
@click.option("--expected-count",
              "-e",
              help="Expected count for each capture",
              default=40,
              type=int)
@click.pass_context
def datalist(ctx, tail, expected_count):
    """
    List the data folders
    """
    import os
    ppath = ctx.obj["ppath"]
    basedir = ppath.basedir
    dfolders = sorted(basedir.glob("*_*Image"))
    folder_count = len(dfolders)
    if tail is not None:
        dfolders = dfolders[-tail:]

    # Count the number of files
    fcounts = []
    for d in dfolders:
        fcount = len(list(d.glob("*.tif*")))
        finished = "X" if fcount == expected_count else ""
        fcounts.append([fcount, finished])

    # Print out the info
    print(("Displaying names of {}/{} captures".format(len(dfolders),
                                                       folder_count)))
    print("Folder name            TIF Counts     FINISHED")
    print("===========            ==========     ========")
    for folder, fcount in zip(dfolders, fcounts):
        finished = "X" if fcount == expected_count else ""
        print(("{:<25}{:<15}{:<10}".format(folder.name, *fcount)))


peemcli.add_command(drift)
peemcli.add_command(datalist)
peemcli.add_command(xmcdlist)
peemcli.add_command(xmcdavg)

if __name__ == "__main__":
    peemcli()
