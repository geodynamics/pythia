
from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages

setup(
    
    name = 'pythia', 
    version = '0.8.1.0',

    zip_safe = False,
    packages = find_packages(),
    # include everything under version control
    include_package_data = True,
    
    install_requires = [
    'Cheetah',
    ],
    extras_require = {
    'acis':     [],
    'blade':    [],
    'elc':      [],
    'journal':  [],
    'mpi':      [],
    'opal':     [],
    'pulse':    [],
    'pyre':     [],
    'rigid':    [],
    },
    
    author = 'Michael A.G. Aivazis',
    author_email = 'aivazis@caltech.edu',
    description = 'An extensible, object-oriented framework for specifying and staging complex, multi-physics simulations.',
    license = 'BSD',
    url = 'http://www.geodynamics.org/cig/software/packages/pythia/',
    download_url = 'http://crust.geodynamics.org/~leif/shipping/', # temporary
    
    )
