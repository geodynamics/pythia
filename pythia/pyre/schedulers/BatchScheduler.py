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


from .Scheduler import Scheduler


class BatchScheduler(Scheduler):

    import pythia.pyre.inventory

    # override the default for 'wait'
    wait = pythia.pyre.inventory.bool("wait", default=False)
    wait.meta['tip'] = """wait for the job to finish"""


# end of file
