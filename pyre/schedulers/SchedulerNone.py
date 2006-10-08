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


from Scheduler import Scheduler


class SchedulerNone(Scheduler):

    
    name = "scheduler-none"

    
    def schedule(self, job):
        import os, sys

        job.executable = os.path.abspath(job.executable)
        
        argv = [job.executable] + job.arguments
        
        if self.dry:
            print ' '.join(argv)
            return

        mode = 0
        if self.wait:
            mode |= os.P_WAIT
        else:
            mode |= os.P_NOWAIT
        ret = os.spawnvp(mode, argv[0], argv)
        if self.wait:
            if ret != 0:
                sys.exit("%s: %s: exit %d" % (sys.argv[0], argv[0], ret))
        else:
            self._info.log("%s: spawned process %d: %r" % (sys.argv[0], ret, argv))
        
        return


# end of file 
