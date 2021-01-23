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


class Job(Component):

    name = "job"

    import pythia.pyre.inventory
    import pythia.pyre.util
    from pythia.pyre.units.time import minute

    task = pythia.pyre.inventory.str("name")  # 'task' internally, to avoid name conflict

    queue = pythia.pyre.inventory.str("queue")
    mail = pythia.pyre.inventory.bool("mail", default=False)
    dwalltime = pythia.pyre.inventory.dimensional("walltime", default=0 * minute)

    stdin = pythia.pyre.inventory.str("stdin", default=pythia.pyre.util.devnull())
    stdout = pythia.pyre.inventory.str("stdout", default="stdout.txt")
    stderr = pythia.pyre.inventory.str("stderr", default="stderr.txt")

    environment = pythia.pyre.inventory.list("environment")

    executable = pythia.pyre.inventory.str("executable")
    arguments = pythia.pyre.inventory.list("arguments")

    comments = pythia.pyre.inventory.list("comments")

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
