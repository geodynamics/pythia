
from archimedes import use_merlin
use_merlin()

from merlin import setup, find_packages

setup(
    
    name = 'pythia', 
    version = '0.8.1.1',

    zip_safe = False,
    packages = find_packages(),
    # include everything under version control
    include_package_data = True,
    
    install_requires = [
    'Cheetah',
    ],

    extras_require = {

    # * acis: "a set of Python bindings for ACIS, the solid modeler from Spatial"
    # In the old 'configure' script, the following was toggled using
    # '--with-acis'.  ACIS had to be installed for it to build.
    'acis':     [],

    # * blade: "a generalization of Glade, the popular user interface builder for Gtk+"
    # Does this introduce any dependencies?
    'blade':    [],
    
    # In the old 'configure' script, the following were all toggled
    # together using '--with-mpi'.  Do they all depend only on MPI?
    # If so, perhaps it should be a single "extra".
    'elc':      [],
    'mpi':      [], ### This is the only "extra" currently supported by CIG-Pythia. ###
    'pulse':    [],
    'rigid':    [],
    
    # Standalone, but might depend upon Django someday :-)
    'opal':    [],
    },
    
    author = 'Michael A.G. Aivazis',
    author_email = 'aivazis@caltech.edu',
    description = 'An extensible, object-oriented framework for specifying and staging complex, multi-physics simulations.',
    license = 'BSD',
    url = 'http://www.geodynamics.org/cig/software/packages/cs/pythia/',
    
    )
