from distutils.core import setup
import setuptools

setup(
    name='git_empty_dirs',         # How you named your package folder
    packages=setuptools.find_packages(),   # Chose the same as "name"
    version='0.4',      # Start with a small number and increase it with every change you make
    # scripts=['git_empty_dirs'],
    entry_points= {
        'console_scripts': [
            'git_empty_dirs = git_empty_dirs.__main__:main',
        ]
    },
    # Choose a license from here: https://help.github.com/articles/licensing-a-repository
    license='gpl-2.0',
    # Give a short description about your library
    description='Committing Empty Directories to Git :joy::joy::relaxed::relaxed:',
    author='Meet Parikh',                   # Type in your name
    author_email='meet.parikh@gmail.com',      # Type in your E-Mail
    # Provide either the link to your repository or to your website
    url='https://github.com/ParikhMeet/GitEmptyDirs',
    # Release url from repository
    download_url='https://github.com/ParikhMeet/GitEmptyDirs/archive/v0.4.tar.gz',
    # Keywords that define your package best
    keywords=['Git', 'Empty', 'Directory', 'Directories', 'Folder'],
    install_requires=[            # External libraries
    ],
    classifiers=[
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Development Status :: 5 - Production/Stable',
        # Define that your audience are developers
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        # Again, pick a license
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        # Specify which python versions that you want to support
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
