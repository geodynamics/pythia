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
        from pkg_resources import resource_filename
        
        jobstart = resource_filename("pyre", "scripts/jobstart.py")
        entry = self.entryName()
        argv = self.getArgv(*args, **kwds)
        
        # initialize the job
        job = self.job
        job.nodes = self.nodes
        job.executable = self.executable
        job.arguments = [jobstart, entry] + argv

        # schedule
        self.scheduler.schedule(job)
        
        return


    def onLauncherNode(self, *args, **kwds):
        import sys
        from pkg_resources import resource_filename

        mpistart = resource_filename(__name__, "scripts/mpistart.py")
        entry = self.entryName()
        argv = self.getArgv(*args, **kwds)
        
        # initialize the launcher
        launcher = self.launcher
        launcher.nodes = self.nodes
        self.getNodes()
        launcher.executable = self.executable
        launcher.arguments = [mpistart, entry] + argv
        
        # launch
        launcher.launch()
        
        return


    def onComputeNodes(self, *args, **kwds):
        self.main(*args, **kwds)


    def __init__(self, name=None):
        super(Application, self).__init__(name)

        import sys
        self.executable = sys.executable


# end of file
