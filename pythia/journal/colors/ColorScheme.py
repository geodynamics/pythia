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


class ColorScheme(Component):

    import pythia.pyre.inventory

    filename = pythia.pyre.inventory.str("filename", default="NoColor")
    line = pythia.pyre.inventory.str("line", default="NoColor")
    function = pythia.pyre.inventory.str("function", default="NoColor")
    stackTrace = pythia.pyre.inventory.str("stack-trace", default="NoColor")

    src = pythia.pyre.inventory.str("src", default="NoColor")

    facility = pythia.pyre.inventory.str("facility", default="NoColor")
    severityDebug = pythia.pyre.inventory.str("severity-debug", default="NoColor")
    severityInfo = pythia.pyre.inventory.str("severity-info", default="NoColor")
    severityWarning = pythia.pyre.inventory.str("severity-warning", default="NoColor")
    severityError = pythia.pyre.inventory.str("severity-error", default="NoColor")

    normal = pythia.pyre.inventory.str("normal", default="Normal")

    def __getitem__(self, key):
        return self.getTraitValue(key)


# end of file
