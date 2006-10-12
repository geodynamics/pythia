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


from pyre.launchers.Launcher import Launcher as Base


class Launcher(Base):
    
    
    import pyre.inventory as pyre

    dry = pyre.bool("dry", default=False)
    dry.meta['tip'] = "prints the command line and exits"
        
    nodegen = pyre.str("nodegen")
    nodegen.meta['tip'] = """a printf-style format string, used in conjunction with 'nodelist' to generate the list of machine names (e.g., "n%03d")"""
        
    extra = pyre.str("extra")
    extra.meta['tip'] = "extra arguments to pass to mpirun"
        
    command = pyre.str("command", default="mpirun")


    def launch(self):
        import os, sys

        self.executable = os.path.abspath(self.executable)

        argv = self._buildArgumentList()
        if not argv:
            return self.dry
        
        command = ' '.join(argv)
        
        if self.dry:
            print command
            return True
        
        self._info.log("spawning: %s" % command)
        status = os.spawnvp(os.P_WAIT, argv[0], argv)
        statusMsg = "%s: %s: exit %d" % (sys.argv[0], argv[0], status)
        if status != 0:
            sys.exit(statusMsg)
        self._info.log(statusMsg)

        return True


    def _buildArgumentList(self):
        if not self.nodes:
            self.nodes = len(self.nodelist)

        if self.nodes < 1:
            self.nodes = 1

        # build the command
        args = self.command.split(' ')
        self._appendMpiRunArgs(args)

        args.append(self.executable)
        args += self.arguments

        return args


    def _appendMpiRunArgs(self, args):
        args.append(self.extra)
        args.extend(['-np', '%d' % self.nodes])
        
        # use only the specific nodes specified explicitly
        if self.nodelist:
            self._appendNodeListArgs(args)


# end of file 
