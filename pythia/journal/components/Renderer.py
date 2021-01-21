#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                             Michael A.G. Aivazis
#                      California Institute of Technology
#                      (C) 1998-2005  All Rights Reserved
#
# <LicenseText>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from pythia.pyre.components.Component import Component


class Renderer(Component):

    class Inventory(Component.Inventory):

        import pythia.pyre.inventory

        header = pythia.pyre.inventory.str(
            "header",
            default=" >> %(filename)s:%(line)s:%(function)s\n -- %(facility)s(%(severity)s)")
        header.meta['tip'] = "the first line of the generated message"

        footer = pythia.pyre.inventory.str("footer", default="")
        footer.meta['tip'] = "the last line of the generated message"

        format = pythia.pyre.inventory.str("format", default=" -- %s")
        format.meta['tip'] = "the format string used to render the message"

    def __init__(self, name="renderer"):
        Component.__init__(self, name, "renderer")
        self.renderer = None
        return

    def _init(self):
        renderer = self.createRenderer()

        renderer.header = self.inventory.header
        renderer.footer = self.inventory.footer
        renderer.format = self.inventory.format

        self.renderer = renderer

        return renderer

    def createRenderer(self):
        from pythia.journal.devices.Renderer import Renderer
        return Renderer()


# version
__id__ = "$Id: Renderer.py,v 1.2 2005/03/10 06:16:37 aivazis Exp $"

# End of file
