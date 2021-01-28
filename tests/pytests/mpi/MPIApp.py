# ======================================================================
#
# Brad T. Aagaard, U.S. Geological Survey
#
# This code was developed as part of the Computational Infrastructure
# for Geodynamics (http://geodynamics.org).
#
# Copyright (c) 2010-2017 University of California, Davis
#
# See COPYING for license information.
#
# ======================================================================
#

import pythia.mpi
from pythia.mpi.Application import Application

class MPIApp(Application):

    def __init__(self, name="mpiapp"):
        Application.__init__(self, name)
        self.nodes = 2

    def log_filename(self, rank):
        return "mpiapp-{}.log".format(rank)
        
    def log_output(self, rank):
        return ["Process: {}, Size: {}\n".format(rank, self.nodes)]

    def main(self, *args, **kwds):
        comm = pythia.mpi.world()
        with open(self.log_filename(comm.rank), "w") as fout:
            for line in self.log_output(comm.rank):
                fout.write(line)


# End of file
