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


class Weaver(Component):

    # inventory
    class Inventory(Component.Inventory):

        import pythia.pyre.inventory

        author = pythia.pyre.inventory.str("author", default="")
        organization = pythia.pyre.inventory.str("organization", default="")
        copyright = pythia.pyre.inventory.str("copyright", default="")

        bannerWidth = pythia.pyre.inventory.int("bannerWidth", default=78)
        bannerCharacter = pythia.pyre.inventory.str("bannerCharacter", default='~')

        creator = pythia.pyre.inventory.str("creator")
        timestamp = pythia.pyre.inventory.bool("timestamp", default=True)

        lastLine = pythia.pyre.inventory.str("lastLine", default=" End of file ")
        copyrightLine = pythia.pyre.inventory.str(
            "copyrightLine", default="(C) %s  All Rights Reserved")
        licenseText = pythia.pyre.inventory.preformatted("licenseText", default=["{LicenseText}"])

        timestampLine = pythia.pyre.inventory.str(
            "timestampLine", default=" Generated automatically by %s on %s")

        versionId = pythia.pyre.inventory.str("versionId", default=' $' + 'Id' + '$')

    def weave(self, document=None, stream=None):
        # produce the text
        text = self.render(document)

        # verify the output stream
        if stream is None:
            import sys
            stream = sys.stdout

        stream.write("\n".join(text))
        stream.write("\n")

        return

    def render(self, document=None):
        self._renderer.options = self.inventory
        ret = self._renderer.weave(document)
        self._renderer.options = None
        return ret

    def begin(self):
        self._renderer.options = self.inventory
        self._renderer.begin()
        return

    def contents(self, body):
        self._renderer.contents(body)
        return

    def end(self):
        self._renderer.end()
        self._renderer.options = None
        return

    def document(self):
        return self._renderer.document()

    def languages(self):
        candidates = sorted(self.inventory.retrieveShelves(address=['mills'], extension='odb'))

        return candidates

    def __init__(self, name=None):
        if name is None:
            name = 'weaver'

        Component.__init__(self, name, facility='weaver')

        self._renderer = None
        self._language = None

        return

    # language property

    def _getLanguage(self):
        return self._language

    def _setLanguage(self, language):
        self._language = language
        self._renderer = self._retrieveLanguage(language)
        return

    def _retrieveLanguage(self, language):
        weaver = self.retrieveComponent(
            factory=self.name, name=language, vault=['mills'])

        if weaver:
            return weaver

        import pythia.journal.diagnostics
        pythia.journal.diagnostics.error('pyre.weaver').log("could not locate weaver for '%s'" % language)

        self.getCurator().dump()

        return None

    language = property(_getLanguage, _setLanguage, None, "")

    # renderer property

    def _getRenderer(self):
        return self._renderer

    def _setRenderer(self, renderer):
        self._renderer = renderer
        return

    renderer = property(_getRenderer, _setRenderer, None, "")


# version
__id__ = "$Id: Weaver.py,v 1.3 2005/03/13 20:59:44 aivazis Exp $"

# End of file
