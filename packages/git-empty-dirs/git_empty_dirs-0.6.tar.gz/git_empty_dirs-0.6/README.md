# GitEmptyDirs !!

Ever came up with a scenario where you have extracted a software platform and initialised a git repository on it so that you can start building things on it ? If in case, the extracted platform contains lot of empty directories, those directories don't get committed to you repository which can lead to lot of errors for your co worker. GitEmptyDirs is helpful in those kind of scenarios. It creates an empty .gitignore file or copies a specified file in all empty folders so that every folder gets committed.

## Installation

Easily install using one simple command:

    pip install git-empty-dirs

## Usage

GitEmptyDirs can be triggered in three ways.

 1. **git_empty_dirs**
		 It uses the current directory as the base directory and creates an empty .gitignore file in all empty directories.
		 
 2. **git_empty_dirs \<path to base folder\>**
		 It uses the path provided as the base directory and creates an empty .gitignore file in all empty directories.
		 
 3. **git_empty_dirs \<path to base folder\> \<path to sample file\>**
		 It uses the path provided as the base directory and copies the sample file in all empty directories.
