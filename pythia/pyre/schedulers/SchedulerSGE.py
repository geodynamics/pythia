#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                      California Institute of Technology
#                        (C) 2008  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from .BatchScheduler import BatchScheduler
import os
import sys


class SchedulerSGE(BatchScheduler):

    name = "sge"

    import pythia.pyre.inventory

    command = pythia.pyre.inventory.str("command", default="qsub")
    peName = pythia.pyre.inventory.str("pe-name", default="mpi")
    peNumber = pythia.pyre.inventory.str("pe-number", default="n")
    qsubOptions = pythia.pyre.inventory.list("qsub-options")

    def schedule(self, job):
        import pythia.pyre.util as util

        # Fix-up the job.
        if not job.task:
            job.task = "jobname"
        job.walltime = util.hms(job.dwalltime.value)
        job.arguments = ' '.join(job.arguments)

        # Generate the main SGE batch script.
        script = self.retrieveTemplate('batch.sh', ['schedulers', 'scripts', self.name])
        if script is None:
            self._error.log("could not locate batch script template for '%s'" % self.name)
            sys.exit(1)

        script.scheduler = self
        script.job = job

        if self.dry:
            print(script)
            return

        try:
            import os
            import tempfile

            filename = tempfile.mktemp()
            with open(filename, "w") as s:
                s.write("%s" % script)

            cmd = [self.command, filename]
            self._info.log("spawning: %s" % ' '.join(cmd))
            status = os.spawnvp(os.P_WAIT, cmd[0], cmd)

            os.remove(filename)

            exitStatus = None
            if (os.WIFSIGNALED(status)):
                statusStr = "signal %d" % os.WTERMSIG(status)
            elif (os.WIFEXITED(status)):
                exitStatus = os.WEXITSTATUS(status)
                statusStr = "exit %d" % exitStatus
            else:
                statusStr = "status %d" % status
            self._info.log("%s: %s" % (cmd[0], statusStr))

        except IOError as e:
            self._error.log("%s: %s" % (self.command, e))
            return

        if exitStatus == 0:
            pass
        else:
            sys.exit("%s: %s: %s" % (sys.argv[0], cmd[0], statusStr))
        return

    def jobId(cls):
        return os.environ['JOB_ID']
    jobId = classmethod(jobId)


# end of file
