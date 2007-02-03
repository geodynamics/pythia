# Setup configuration is in setup.cfg.

import setuptools
setuptools.setup()
=======

from distutils.core import setup

setup(
    
    name = 'nemesis', 
    version = '1.1',

    zip_safe = False,
    
    author = 'Leif Strand',
    author_email = 'leif@geodynamics.org',
    description = """A Python interpreter which embeds MPI.""",
    license = 'BSD',
    url = 'http://www.geodynamics.org/cig/software/pythia/',

)
