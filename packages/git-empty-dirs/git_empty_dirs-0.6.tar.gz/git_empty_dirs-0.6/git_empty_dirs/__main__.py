#!/usr/bin/env python

import os
from sys import argv
from shutil import copy2


def main():
    dirName = argv[1] if len(argv) > 1 else os.getcwd()
    listOfEmptyDirs = [dirpath for (dirpath, dirnames, filenames) in os.walk(
        dirName) if len(dirnames) == 0 and len(filenames) == 0]

    if len(listOfEmptyDirs) == 0:
        print("No empty directories found.")
    else:
        print("Found following empty directories")
        for elem in listOfEmptyDirs:
            print(elem)
            if len(argv) > 2:
                try:
                    copy2(argv[2], elem)
                except:
                    print("Could not copy file.")
                    break
            else:
                open(os.path.join(elem, ".gitignore"), 'a').close()


if __name__ == '__main__':
    main()
