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


class ColorScheme(Component):

    import pyre.inventory

    filename = pyre.inventory.str("filename", default="NoColor")
    line = pyre.inventory.str("line", default="NoColor")
    function = pyre.inventory.str("function", default="NoColor")
    stackTrace = pyre.inventory.str("stack-trace", default="NoColor")

    src = pyre.inventory.str("src", default="NoColor")

    facility = pyre.inventory.str("facility", default="NoColor")
    severityDebug = pyre.inventory.str("severity-debug", default="NoColor")
    severityInfo = pyre.inventory.str("severity-info", default="NoColor")
    severityWarning = pyre.inventory.str("severity-warning", default="NoColor")
    severityError = pyre.inventory.str("severity-error", default="NoColor")

    normal = pyre.inventory.str("normal", default="Normal")

    def __getitem__(self, key):
        return self.getTraitValue(key)


# end of file
