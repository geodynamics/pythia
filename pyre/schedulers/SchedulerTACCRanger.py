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


from .SchedulerSGE import SchedulerSGE
import os
import sys


class SchedulerTACCRanger(SchedulerSGE):

    name = "tacc-ranger"

    import pyre.inventory

    command = pyre.inventory.str("command", default="qsub")
    tpn = pyre.inventory.int("tpn", default=16,
                             validator=pyre.inventory.choice([1, 2, 4, 8, 12, 15, 16]))
    tpn.meta['tip'] = 'Task per node'
    qsubOptions = pyre.inventory.list("qsub-options")

    def schedule(self, job):
        from math import ceil
        # round up to multiple of 16
        nodes = ceil(job.nodes / float(self.tpn))
        self.cores = int(nodes * 16)

        SchedulerSGE.schedule(self, job)

# end of file
