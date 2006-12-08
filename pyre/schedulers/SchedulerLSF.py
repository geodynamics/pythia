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


from BatchScheduler import BatchScheduler


class SchedulerLSF(BatchScheduler):
    
    
    name = "lsf"
    

    import pyre.inventory as pyre
    
    command         = pyre.str("command", default="mpijob mpirun")
    batchCommand    = pyre.str("batch-command", default="bsub")
    bsubOptions     = pyre.list("bsub-options")
    
    
    def schedule(self, job):
        import os, sys
        import pyre.util as util

        # Fix-up the job.
        if not job.task:
            # LSF scripts must have a job name; otherwise strange
            # "/bin/sh: Event not found" errors occur (tested on
            # TACC's Lonestar system).
            job.task = "jobname"
        job.walltime = util.hms(job.dwalltime.value)
        job.arguments = ' '.join(job.arguments)
        
        # Generate the main LSF batch script.
        script = self.retrieveTemplate('batch.sh', ['schedulers', 'scripts', 'lsf'])
        script.scheduler = self
        script.job = job
        
        if self.dry:
            print script
            return

        try:
            import os
            from popen2 import Popen4

            cmd = [self.batchCommand]
            if self.wait:
                cmd.append("-K")
            self._info.log("spawning: %s" % ' '.join(cmd))
            child = Popen4(cmd)
            self._info.log("spawned process %d" % child.pid)

            print >> child.tochild, script
            child.tochild.close()

            if self.wait:
                self._info.log("Waiting for dispatch...")

            for line in child.fromchild:
                self._info.line("    " + line.rstrip())
            status = child.wait()
            self._info.log()

            exitStatus = None
            if (os.WIFSIGNALED(status)):
                statusStr = "signal %d" % os.WTERMSIG(status)
            elif (os.WIFEXITED(status)):
                exitStatus = os.WEXITSTATUS(status)
                statusStr = "exit %d" % exitStatus
            else:
                statusStr = "status %d" % status
            self._info.log("%s: %s" % (cmd[0], statusStr))
        
        except IOError, e:
            self._error.log("%s: %s" % (self.batchCommand, e))
            return
        
        # "[When given the -K option], bsub will exit with the same
        # exit code as the job so that job scripts can take
        # appropriate actions based on the exit codes. bsub exits with
        # value 126 if the job was terminated while pending."
        if exitStatus == 126:
            pass
        elif self.wait:
            sys.exit(exitStatus)
        
        if exitStatus == 0:
            pass
        else:
            sys.exit("%s: %s: %s" % (sys.argv[0], cmd[0], statusStr))
        
        return


# end of file 
