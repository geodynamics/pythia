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


from pyre.applications.Script import Script


class Application(Script):


    import pyre.inventory
    nodes = pyre.inventory.int("nodes", default=1)

    import pyre.schedulers
    scheduler = pyre.schedulers.scheduler("scheduler", default="none")
    job = pyre.schedulers.job("job")
        
    import pyre.launchers
    launcher = pyre.launchers.facility("launcher", default="mpich")


    nodes.meta['tip'] = """number of machine nodes"""


    def execute(self, *args, **kwds):
        self.onLoginNode(*args, **kwds)


    def onLoginNode(self, *args, **kwds):
        import sys
        
        path = self.pathString()
        requires = self.requires()
        entry = self.entryName()
        argv = self.getArgv(*args, **kwds)
        
        # initialize the job
        job = self.job
        job.nodes = self.nodes
        job.executable = self.jobExecutable
        job.arguments = ["--pyre-start", path, requires, "pyre.schedulers:jobstart", entry] + argv

        # schedule
        self.scheduler.schedule(job)
        
        return


    def onLauncherNode(self, *args, **kwds):
        import sys

        path = self.pathString()
        requires = self.requires()
        entry = self.entryName()
        argv = self.getArgv(*args, **kwds)
        
        # initialize the launcher
        launcher = self.launcher
        launcher.nodes = self.nodes
        launcher.executable = self.mpiExecutable
        launcher.arguments = ["--pyre-start", requires, path, "mpi:mpistart", entry] + argv
        
        # launch
        launcher.launch()
        
        return


    def onComputeNodes(self, *args, **kwds):
        self.main(*args, **kwds)


    def __init__(self, name=None):
        super(Application, self).__init__(name)

        import sys
        from os.path import join, split

        self.executable = sys.executable
        exe = split(self.executable)
        self.jobExecutable = self.executable
        self.mpiExecutable = join(exe[0], "mpi" + exe[1])


# end of file
