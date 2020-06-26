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

import unittest
import os

from pyre.applications.Script import Script
import pyre.inventory


from pyre.units.time import hour


class TestJob(unittest.TestCase):

    def test_defaults(self):
        app = JobApp()
        app.run(argv=["jobapp"])

        self.assertEqual("", app.data["name"])
        self.assertEqual("", app.data["queue"])
        self.assertFalse(app.data["mail"])
        self.assertEqual(0 * hour, app.data["walltime"])
        self.assertEqual("stdout.txt", app.data["stdout"])
        self.assertEqual("stderr.txt", app.data["stderr"])
        self.assertEqual(0, len(app.data["environment"]))
        self.assertEqual("", app.data["executable"])
        self.assertEqual(0, len(app.data["args"]))
        self.assertEqual(0, len(app.data["comments"]))

    def test_custom(self):
        ARGS = [
            "--job.name=newjob",
            "--job.queue=short",
            "--job.mail",
            "--job.walltime=1*hour",
            "--job.stdout=job.out",
            "--job.stderr=job.err",
            "--job.environment=[go there, everywhere]",
            "--job.executable=/bin/doit",
            "--job.arguments=[yes, no, maybe]",
            "--job.comments=[one, two, three]",
        ]
        app = JobApp()
        app.run(argv=["jobapp"] + ARGS)

        self.assertEqual("newjob", app.data["name"])
        self.assertEqual("short", app.data["queue"])
        self.assertTrue(app.data["mail"])
        self.assertEqual(1 * hour, app.data["walltime"])
        self.assertEqual("job.out", app.data["stdout"])
        self.assertEqual("job.err", app.data["stderr"])
        self.assertEqual(2, len(app.data["environment"]))
        for valueE, value in zip(["go there", "everywhere"], app.data["environment"]):
            self.assertEqual(valueE, value)
        self.assertEqual("/bin/doit", app.data["executable"])
        self.assertEqual(3, len(app.data["args"]))
        for valueE, value in zip(["yes", "no", "maybe"], app.data["args"]):
            self.assertEqual(valueE, value)
        self.assertEqual(3, len(app.data["comments"]))
        for valueE, value in zip(["one", "two", "three"], app.data["comments"]):
            self.assertEqual(valueE, value)


class JobApp(Script):

    debug = pyre.inventory.bool("debug", default=False)

    from pyre.schedulers.Job import Job
    job = pyre.inventory.facility("job", factory=Job)

    def __init__(self, name="jobapp"):
        Script.__init__(self, name)

    def main(self, *args, **kwds):
        self.data = {
            "name": self.job.task,
            "queue": self.job.queue,
            "mail": self.job.mail,
            "walltime": self.job.dwalltime,
            "stdout": self.job.stdout,
            "stderr": self.job.stderr,
            "environment": self.job.environment,
            "executable": self.job.executable,
            "args": self.job.arguments,
            "comments": self.job.comments,
        }
        if self.debug:
            print(self.data)


class TestScheduler(unittest.TestCase):

    def run_app(self, executable="", arguments=[], dry=False, ):
        app = SchedulerApp()
        args = [
            "--scheduler={}".format(self.scheduler),
            "--scheduler.dry={}".format(dry),
            "--job.executable={}".format(executable),
            "--job.arguments={}".format(arguments),
        ]
        app.run(argv=["schedulerapp"] + args)
        self.app = app
        self.scheduler = app.scheduler
        self.job = app.job


class TestNone(TestScheduler):

    scheduler = "none"

    def test_defaults(self):
        self.run_app()
        self.assertFalse(self.scheduler.dry)
        self.assertTrue(self.scheduler.wait)
        self.assertEqual("/bin/sh", self.scheduler.shell)

    def test_jobId(self):
        self.run_app()
        jid = self.scheduler.jobId()
        self.assertGreater(int(jid), 0)

    def test_dry(self):
        self.run_app(dry=True)
        self.scheduler.schedule(self.job)

    def test_schedule(self):
        self.run_app(executable="/bin/echo", arguments=["abc"])
        self.scheduler.schedule(self.job)


class TestLSF(TestScheduler):

    scheduler = "lsf"

    def test_defaults(self):
        self.run_app()
        self.assertFalse(self.scheduler.dry)
        self.assertFalse(self.scheduler.wait)
        self.assertEqual("/bin/sh", self.scheduler.shell)
        self.assertEqual("bsub", self.scheduler.command)
        self.assertEqual(0, len(self.scheduler.bsubOptions))

    def test_jobId(self):
        JOB_ID = "54224"

        os.environ["LSB_JOBID"] = JOB_ID
        self.run_app()
        jid = self.scheduler.jobId()
        self.assertEqual(JOB_ID, jid)

    def test_dry(self):
        self.run_app(dry=True)
        self.scheduler.schedule(self.job)

    def test_schedule(self):
        self.run_app()
        with self.assertRaises(SystemExit):
            self.scheduler.schedule(self.job)


class TestPBS(TestScheduler):

    scheduler = "pbs"

    def test_defaults(self):
        self.run_app()
        self.assertFalse(self.scheduler.dry)
        self.assertFalse(self.scheduler.wait)
        self.assertEqual("/bin/sh", self.scheduler.shell)
        self.assertEqual("qsub", self.scheduler.command)
        self.assertEqual(0, len(self.scheduler.qsubOptions))
        self.assertEqual(0, len(self.scheduler.resourceList))
        self.assertEqual(1, self.scheduler.ppn)

    def test_jobId(self):
        JOB_ID = "5435"

        os.environ["PBS_JOBID"] = JOB_ID
        self.run_app()
        jid = self.scheduler.jobId()
        self.assertEqual(JOB_ID, jid)

    def test_dry(self):
        self.run_app(dry=True)
        self.scheduler.schedule(self.job)

    def test_schedule(self):
        self.run_app()
        with self.assertRaises(SystemExit):
            self.scheduler.schedule(self.job)


class TestSGE(TestScheduler):

    scheduler = "sge"

    def test_defaults(self):
        self.run_app()
        self.assertFalse(self.scheduler.dry)
        self.assertFalse(self.scheduler.wait)
        self.assertEqual("/bin/sh", self.scheduler.shell)
        self.assertEqual("qsub", self.scheduler.command)
        self.assertEqual("mpi", self.scheduler.peName)
        self.assertEqual("n", self.scheduler.peNumber)
        self.assertEqual(0, len(self.scheduler.qsubOptions))

    def test_jobId(self):
        JOB_ID = "10655"

        os.environ["JOB_ID"] = JOB_ID
        self.run_app()
        jid = self.scheduler.jobId()
        self.assertEqual(JOB_ID, jid)

    def test_dry(self):
        self.run_app(dry=True)
        self.scheduler.schedule(self.job)

    def test_schedule(self):
        self.run_app()
        with self.assertRaises(SystemExit):
            self.scheduler.schedule(self.job)


class TestTACCRanger(TestScheduler):

    scheduler = "tacc-ranger"

    def test_defaults(self):
        self.run_app()
        self.assertFalse(self.scheduler.dry)
        self.assertFalse(self.scheduler.wait)
        self.assertEqual("/bin/sh", self.scheduler.shell)
        self.assertEqual(16, self.scheduler.tpn)
        self.assertEqual(0, len(self.scheduler.qsubOptions))

    def test_jobId(self):
        JOB_ID = "45892"

        os.environ["JOB_ID"] = JOB_ID
        self.run_app()
        jid = self.scheduler.jobId()
        self.assertEqual(JOB_ID, jid)

    def test_dry(self):
        self.run_app(dry=True)
        self.scheduler.schedule(self.job)

    def test_schedule(self):
        self.run_app()
        with self.assertRaises(SystemExit):
            self.scheduler.schedule(self.job)


class SchedulerApp(Script):

    import pyre.schedulers
    scheduler = pyre.schedulers.scheduler("scheduler", default="none")

    from pyre.schedulers.Job import Job
    job = pyre.inventory.facility("job", factory=Job)

    def __init__(self, name="schedulerapp"):
        Script.__init__(self, name)

    def main(self, *args, **kwds):
        pass


def test_classes():
    return [TestJob, TestNone, TestLSF, TestPBS, TestSGE, TestTACCRanger]


if __name__ == "__main__":
    suite = unittest.TestSuite()
    for cls in test_classes():
        suite.addTest(unittest.makeSuite(cls))
    unittest.TextTestRunner(verbosity=2).run(suite)


# End of file
