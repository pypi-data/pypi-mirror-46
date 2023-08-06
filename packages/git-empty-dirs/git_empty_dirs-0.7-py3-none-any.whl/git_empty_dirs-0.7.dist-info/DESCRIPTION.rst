# GitEmptyDirs !!

Ever came up with a scenario where you have extracted a software platform and initialised a git repository on it so that you can start building things on it ? If in case, the extracted platform contains lot of empty directories, those directories don't get committed to you repository which can lead to lot of errors for your co worker. GitEmptyDirs is helpful in those kind of scenarios. It creates an empty .gitignore file or copies a specified file in all empty folders so that every folder gets committed.

## Installation  

Easily install using one simple command:

    pip install git-empty-dirs

## Usage

GitEmptyDirs can be triggered in below ways.  

1.  **git_empty_dirs**

It uses the current directory as the base directory and creates an empty .gitignore file in all empty directories.

2.  **git_empty_dirs  -b \<path  to  base  folder\>**

It uses the path provided as the base directory and creates an empty .gitignore file in all empty directories.

3.  **git_empty_dirs -s \<path  to  sample  file\>**

It uses the current directory as the base directory and copies the sample file in all empty directories.

4.  **git_empty_dirs  -b \<path  to  base  folder\> -s \<path  to  sample  file\>**

It uses the path provided as the base directory and copies the sample file in all empty directories.


For help please invoke **git_empty_dirs -h**

    usage: git_empty_dirs [-h] [-b BASE_DIR] [-s SAMPLE_FILE]

	optional arguments:
	  -h, --help            show this help message and exit
	  -b BASE_DIR, --base-dir BASE_DIR
                        Specify the base directory for searching empty
                        directories
	  -s SAMPLE_FILE, --sample-file SAMPLE_FILE
                        Specify the file to be copied to each empty directory

