""" Setup script. Used by easy_install and pip. """

import os
import sys
import subprocess as sp
import re

from setuptools import setup, find_packages, Command

VERSIONFILE="extasycoco/_version.py"
name="extasycoco"
verstrline = open(VERSIONFILE, "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstrline, re.M)
if mo:
    verstr = mo.group(1)
else:
    raise RunTimeError("Unable to find version string in {}.".format(VERSIONFILE))

#-----------------------------------------------------------------------------
# check python version. we need >= 2.7, or >= 3.4:
if sys.version_info[:2] < (2, 7) or (3, 0) <= sys.version_info[:2] < (3, 4):
    raise RuntimeError("%s requires Python 2.7 or 3.4+" % name)


#-----------------------------------------------------------------------------
#
def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


#-----------------------------------------------------------------------------
setup_args = {
    'name'             : "extasycoco",
    'version'          : verstr,
    'description'      : "EXTASY Project - CoCo",
    'long_description' : "ExTASY Project - CoCo : molecular ensemble analysis and enhancement.",
    'author'           : "The EXTASY Project",
    'author_email'     : "charles.laughton@nottingham.ac.uk",
    'url'              : "https://bitbucket.org/extasy-project/extasy-project",
    'download_url'     : "https://bitbucket.org/extasy-project/coco/get/"+verstr+".tar.gz",
    'license'          : "BSD",
    'classifiers'      : [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Scientific/Engineering',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Operating System :: Unix'
    ],

    'packages'    : find_packages(),
    'scripts' : ['scripts/pyCoCo', 'scripts/pyCoCoDM'],
    'install_requires' : ['numpy',
                          'scipy',
                          'pypcazip>=2.0.0',
                          'scikit-image',
                          'scikit-learn',
    		          'mdio'],
    'zip_safe'         : False,
}

#-----------------------------------------------------------------------------

setup (**setup_args)
