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


from pyre.components import Component


class Job(Component):

    name = "job"

    import pyre.inventory
    import pyre.util
    from pyre.units.time import minute

    task = pyre.inventory.str("name")  # 'task' internally, to avoid name conflict

    queue = pyre.inventory.str("queue")
    mail = pyre.inventory.bool("mail", default=False)
    dwalltime = pyre.inventory.dimensional("walltime", default=0 * minute)

    stdin = pyre.inventory.str("stdin", default=pyre.util.devnull())
    stdout = pyre.inventory.str("stdout", default="stdout.txt")
    stderr = pyre.inventory.str("stderr", default="stderr.txt")

    environment = pyre.inventory.list("environment")

    executable = pyre.inventory.str("executable")
    arguments = pyre.inventory.list("arguments")

    comments = pyre.inventory.list("comments")

    def __init__(self):
        super(Job, self).__init__()
        self.nodes = 1
        self.id = None

    def getStateArgs(self, stage):
        state = []
        if stage == 'launch':
            state.append("--macros.job.name=%s" % self.task)
        elif stage == 'compute':
            state.append("--macros.job.id=%s" % self.id)
        return state


# end of file
