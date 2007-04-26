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
        state = self.getStateArgs() + self.job.getStateArgs()
        
        # initialize the job
        job = self.job
        job.nodes = self.nodes
        job.executable = self.jobExecutable
        job.arguments = ["--pyre-start", path, requires, "pyre.schedulers:jobstart", entry] + argv + state

        # for debugging purposes, add 'mpirun' command as a comment
        launcher = self.prepareLauncher()
        job.comments.extend(["[%s] %s" % (launcher.name, comment) for comment in launcher.comments()])

        # schedule
        self.scheduler.schedule(job)
        
        return


    def prepareLauncher(self, *args, **kwds):
        import sys

        path = self.pathString()
        requires = self.requires()
        entry = self.entryName()
        argv = self.getArgv(*args, **kwds)
        state = self.getStateArgs() + self.job.getStateArgs()
        
        # initialize the launcher
        launcher = self.launcher
        launcher.nodes = self.nodes
        launcher.executable = self.mpiExecutable
        launcher.arguments = ["--pyre-start", path, requires, "mpi:mpistart", entry] + argv + state

        return launcher

    
    def onLauncherNode(self, *args, **kwds):

        launcher = self.prepareLauncher()

        # launch
        launcher.launch()
        
        return


    def onComputeNodes(self, *args, **kwds):
        self.main(*args, **kwds)


    def getStateArgs(self):
        state = []
        state.append("--nodes=%d" % self.nodes) # in case it was computed
        # define macros
        state.append("--macros.nodes=%d" % self.nodes)
        return state


    def __init__(self, name=None):
        super(Application, self).__init__(name)

        import sys
        from os.path import join, split

        self.executable = sys.executable
        exe = split(self.executable)
        self.jobExecutable = self.executable
        self.mpiExecutable = join(exe[0], "mpi" + exe[1])


# end of file
