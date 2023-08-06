"""
Simple program for watching the data folders
"""

import os
import time
import sys
from peempy import ppath


def main():
    if "-h" in sys.argv:
        print(
            "This programe prints out the folder and file counts in data directory.\n"
        )
        print("Enjoy! By Bonan")
        sys.exit()

    if len(sys.argv) > 1:
        if sys.argv[1] == "all":
            last = None
        else:
            last = int(sys.argv[1])
    else:
        last = 50

    def read_file_count():
        dpath = ppath.basedir

        dfolders = [
            folder for folder in os.listdir(dpath)
            if "_PCOImage" in folder or "_UViewImage" in folder
        ]
        dfolders.sort()

        if len(dfolders) == 0:
            print("No valid data folder found. exit")
            sys.exit(0)

        if last is not None:
            dfolders = dfolders[-last:]

        fcount = []
        for d in dfolders:
            fcount.append(len(os.listdir(os.path.join(dpath, d))))
        return dfolders, fcount

    folders, fcounts = read_file_count()
    print("\nPEEM Acquisition Data\n\n")
    print("{:<20}{:<8}{:<8}".format("Acquisition Folder", "Count", "Norm?"))
    print("-" * 36)

    def print_info(folders, fcount, r_last=False):
        """Print a series of folders names and number of files in there
        :parameter: r_last : print the last line using \r end for constant updating"""
        nlines = len(folders)
        linecount = 1
        for f, c in zip(folders, fcount):
            if c is 50:
                mark = "X"
            else:
                mark = ""
            if r_last and linecount == nlines:
                # This is the last line

                print("{:<20}{:<8}{:<8}".format(f, c, mark), end="\r")
            else:
                print("{:<20}{:<8}{:<8}".format(f, c, mark))
            linecount += 1

    print_info(folders, fcounts, True)

    # Now start to watch the folders
    last_folder = folders[-1]
    while True:
        folders, fcounts = read_file_count()
        if folders[-1] != last_folder:
            ind = folders.index(last_folder)
            print_info(folders[ind:], fcounts[ind:], True)
        else:
            # Here we just update the last line
            print("{:<20}{:<8}{:<8}".format(last_folder, fcounts[-1], ""),
                  end="\r")
        last_folder = folders[-1]
        time.sleep(3)
    return
