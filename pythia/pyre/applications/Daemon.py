#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                             Michael A.G. Aivazis
#                      California Institute of Technology
#                      (C) 1998-2005  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from .Stager import Stager


class Daemon(Stager):

    def execute(self, *args, **kwds):
        self.args = args
        self.kwds = kwds

        try:
            spawn = self.kwds['spawn']
        except KeyError:
            spawn = True

        if not spawn:
            print(" ** daemon %r in debug mode" % self.name)
            import os
            self.daemon(os.getpid(), spawn=False)
            return

        import pythia.pyre.util
        return pythia.pyre.util.spawn(self.done, self.respawn)

    def done(self, pid):
        return

    def respawn(self, pid):
        import os
        os.chdir("/")
        os.setsid()
        os.umask(0)

        import pythia.pyre.util
        pythia.pyre.util.spawn(self.exit, self.daemon)

        return

    def exit(self, pid):
        import sys
        sys.exit(0)

        # unreachable
        import pythia.journal.diagnostics
        pythia.journal.diagnostics.firewall("pyre.services").log("UNREACHABLE")
        return

    def daemon(self, pid, spawn=True):
        import os
        import pythia.journal.diagnostics

        # change the working directory to my home directory
        if not os.path.exists(self.home):
            pythia.journal.diagnostics.error(self.name).log("directory %r does not exist" % self.home)
            self.home = '/tmp'

        os.chdir(self.home)

        # redirect the pythia.journal output since we are about to close all the
        # standard file descriptors
        # currently disabled since a better strategy is to have the application author
        # build a pythia.journal configuration file
        # self.configureJournal()

        if spawn:
            # close all ties with the parent process
            os.close(2)
            os.close(1)
            os.close(0)

            # launch the application
            try:
                self.main(*self.args, **self.kwds)
            except KeyboardInterrupt:
                pythia.journal.diagnostics.error(self.name).log("interrupt")
            except Exception as e:
                import traceback
                pythia.journal.diagnostics.error(self.name).log("exception:\n%s" % traceback.format_exc())
        else:
            # debug mode
            self.main(*self.args, **self.kwds)

        return

    def configureJournal(self):
        # open the logfile
        stream = open(self.name + '.log', "w")

        # attach it as the pythia.journal device
        import pythia.journal.devices
        pythia.journal.devices.logfile(stream)

        return

    def __init__(self):
        self.args = ()
        self.kwds = {}

        self.home = '/tmp'

        return


# version
__id__ = "$Id: Daemon.py,v 1.4 2005/03/11 07:02:54 aivazis Exp $"

# End of file
