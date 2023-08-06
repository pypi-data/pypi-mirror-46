#!/usr/bin/env python

import os
from shutil import copy2
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-b", "--base-dir", help="Specify the base directory for searching empty directories", default=os.getcwd())
    parser.add_argument(
        "-s", "--sample-file", help="Specify the file to be copied to each empty directory")
    args = parser.parse_args()

    listOfEmptyDirs = [dirpath for (dirpath, dirnames, filenames) in os.walk(
        args.base_dir) if len(dirnames) == 0 and len(filenames) == 0]

    if len(listOfEmptyDirs) == 0:
        print("No empty directories found.")
    else:
        print("Found following empty directories")
        for elem in listOfEmptyDirs:
            print(elem)
            if args.sample_file:
                try:
                    copy2(args.sample_file, elem)
                except Exception as e:
                    print("Could not copy file.")
                    print(e)
                    break
            else:
                open(os.path.join(elem, ".gitignore"), 'a').close()


if __name__ == '__main__':
    main()
