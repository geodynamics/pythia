#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                      California Institute of Technology
#                        (C) 2006  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from Launcher import Launcher


class LauncherMPICH(Launcher):


    name = "mpich"


    import pyre.inventory as pyre

    machinefile = pyre.str("machinefile", default="mpirun.nodes")
    machinefile.meta['tip'] = """filename of machine file"""


    def _appendNodeListArgs(self, args):
        machinefile = self.machinefile
        nodegen = self.nodegen
        file = open(machinefile, "w")
        for node in self.nodelist:
            file.write((nodegen + '\n') % node)
        file.close()
        args.append("-machinefile %s" % machinefile)


# end of file 
