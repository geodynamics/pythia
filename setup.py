
from archimedes import use_merlin
use_merlin()

from merlin import setup, find_packages

setup(
    
    name = 'pythia', 
    version = '0.8.1.8',

    zip_safe = True,
    packages = find_packages(),
    # include everything under version control
    include_package_data = True,

    entry_points = {
        # blade
        # XXX: These vault names don't look right.  And what about blade.pml?
        "pyre.odb.toolkits.gnome": [
            "viewer = blade:inspector", # alias for gnome2
        ],
        "pyre.odb.toolkits.gnome2": [
            "viewer = blade:inspector",
        ],
        "pyre.odb.toolkits.gtk": [
            "viewer = blade:inspector", # alias for gtk2
        ],
        "pyre.odb.toolkits.gtk2": [
            "viewer = blade:inspector",
        ],
        # elc
        "pyre.odb.exchangers": [
            "ice = elc:iceExchanger",
            "mpi = elc:mpiExchanger",
            "serial = elc:serialExchanger",
        ],
        # journal
        "pyre.odb.colors": [
            "dark-bg = journal.colors:darkBg",
            "light-bg = journal.colors:lightBg",
        ],
        "pyre.odb.devices": [
            "color-console = journal.components.ColorConsole:ColorConsole",
            "console = journal.components.Console:Console",
            "file = journal.components.File:File",
            "remote = journal.components.Remote:Remote",
            "xterm = journal.components.ColorConsole:ColorConsole",
            "xterm-color = journal.components.ColorConsole:ColorConsole",
        ],
        # mpi
        "pyre.odb.launchers": [
            "mpich = mpi.LauncherMPICH:LauncherMPICH",
        ],
        # pulse
        "pyre.odb.generators": [
            "heaviside = pulse.HeavisidePulse:HeavisidePulse",
            "bath = pulse.Bath:Bath",
        ],
        # pyre
        "pyre.odb.hooks": [
            "built-in = pyre.hooks:builtInExceptHook",
            "current = pyre.hooks:currentExceptHook",
            "ultraTB = pyre.hooks:ultraTBExceptHook",
        ],
        "pyre.odb.marshallers": [
            "idd-pickler = pyre.idd:pickler",
            "ipa-pickler = pyre.ipa:pickler",
            "journal-pickler = journal:pickler", # ?
        ],
        "pyre.odb.mills": [
            "c = pyre.weaver.mills.CMill:CMill",
            "csh = pyre.weaver.mills.CshMill:CshMill",
            "cxx = pyre.weaver.mills.CxxMill:CxxMill",
            "f77 = pyre.weaver.mills.Fortran77Mill:Fortran77Mill",
            "f90 = pyre.weaver.mills.Fortran90Mill:Fortran90Mill",
            "html = pyre.weaver.mills.HTMLMill:HTMLMill",
            "make = pyre.weaver.mills.MakeMill:MakeMill",
            "perl = pyre.weaver.mills.PerlMill:PerlMill",
            "python = pyre.weaver.mills.PythonMill:PythonMill",
            "sh = pyre.weaver.mills.ShMill:ShMill",
            "tex = pyre.weaver.mills.TeXMill:TeXMill",
            "xml = pyre.weaver.mills.XMLMill:XMLMill",
        ],
        "pyre.odb.schedulers": [
            "lsf = pyre.schedulers.SchedulerLSF:SchedulerLSF",
            "none = pyre.schedulers.SchedulerNone:SchedulerNone",
            "pbs = pyre.schedulers.SchedulerPBS:SchedulerPBS",
            "sge = pyre.schedulers.SchedulerSGE:SchedulerSGE",
            "tacc-ranger = pyre.schedulers.SchedulerTACCRanger:SchedulerTACCRanger",
        ],
    },
    
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
    
    'opal':    [],
    },
    
    author = 'Michael A.G. Aivazis',
    author_email = 'aivazis@caltech.edu',
    description = 'An extensible, object-oriented framework for specifying and staging complex, multi-physics simulations.',
    license = 'BSD',
    url = 'http://www.geodynamics.org/cig/software/packages/cs/pythia/',
    
    )
