
from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages
from pyre import __version__

setup(
    
    name = 'pythia', 
    version = __version__ + "-1.0",

    zip_safe = False,
    packages = find_packages(),
    package_data = {
    # If any package contains *.pml or *.odb files, include them:
    '': ['*.pml', '*.odb'],
    },
    
    author = 'Michael A.G. Aivazis',
    author_email = 'aivazis@caltech.edu',
    description = 'An extensible, object-oriented framework for specifying and staging complex, multi-physics simulations.',
    license = "BSD",
    url = 'http://www.cacr.caltech.edu/projects/pyre/',
    
    )
