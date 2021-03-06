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


from pythia.pyre.components import Component


class Scheduler(Component):

    import pythia.pyre.inventory

    dry = pythia.pyre.inventory.bool("dry", default=False)
    dry.meta['tip'] = """don't actually run the job; just print the batch script"""

    wait = pythia.pyre.inventory.bool("wait", default=True)
    wait.meta['tip'] = """wait for the job to finish"""

    shell = pythia.pyre.inventory.str("shell", default="/bin/sh")
    shell.meta['tip'] = """shell for #! line of batch scripts"""

    def schedule(self, job):
        raise NotImplementedError("class '%s' must override 'schedule'" % self.__class__.__name__)

    def jobId(cls):
        raise NotImplementedError("class '%s' must override 'jobId'" % cls.__name__)
    jobId = classmethod(jobId)


# end of file
