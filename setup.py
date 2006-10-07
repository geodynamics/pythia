
try:
    # If setuptools 0.6b1 or later is installed, run with it.
    from pkg_resources import require
    require("setuptools>=0.6b1")
except:
    from ez_setup import use_setuptools
    use_setuptools()

from setuptools import setup, find_packages
from pyre import __version__

setup(
    
    name = 'pythia', 
    version = __version__ + "-1.0b1",

    zip_safe = False,
    packages = find_packages(),
    package_data = {
    # If any package contains *.pml, *.odb, or *.h files, include them:
    '': ['*.pml', '*.odb', '*.h'],
    },
    
    author = 'Michael A.G. Aivazis',
    author_email = 'aivazis@caltech.edu',
    description = 'An extensible, object-oriented framework for specifying and staging complex, multi-physics simulations.',
    license = "BSD",
    url = 'http://www.cacr.caltech.edu/projects/pyre/',
    
    )
