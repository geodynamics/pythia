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


from ColorScheme import ColorScheme


# facilities and components

def colorScheme(name, **kwds):
    from pyre.inventory.Facility import Facility
    kwds['factory'] = kwds.get('factory', ColorScheme)
    kwds['vault'] = kwds.get('vault', ['colors'])
    kwds['family'] = kwds.get('family', 'colorScheme')
    return Facility(name, **kwds)


# odb factories

def darkBg():
    scheme = ColorScheme("dark-bg")

    # XXX: Currently, .cfg files in a zipped egg don't work.
    scheme.inventory.getTrait("filename").default          = "LightGreen"
    scheme.inventory.getTrait("line").default              = "LightGreen"
    scheme.inventory.getTrait("function").default          = "LightPurple"
    scheme.inventory.getTrait("src").default               = "Yellow"
    scheme.inventory.getTrait("facility").default          = "LightBlue"
    scheme.inventory.getTrait("severity-debug").default    = "LightCyan"
    scheme.inventory.getTrait("severity-info").default     = "LightGreen"
    scheme.inventory.getTrait("severity-error").default    = "LightRed"
    scheme.inventory.getTrait("severity-warning").default  = "Yellow"

    return scheme


def lightBg():
    scheme = ColorScheme("light-bg")
    
    scheme.inventory.getTrait("filename").default          = "Green"
    scheme.inventory.getTrait("line").default              = "Green"
    scheme.inventory.getTrait("function").default          = "Purple"
    scheme.inventory.getTrait("src").default               = "Red"
    scheme.inventory.getTrait("facility").default          = "Blue"
    scheme.inventory.getTrait("severity-debug").default    = "Cyan"
    scheme.inventory.getTrait("severity-info").default     = "Green"
    scheme.inventory.getTrait("severity-error").default    = "Red"
    scheme.inventory.getTrait("severity-warning").default  = "Brown"
    
    return scheme


# end of file 
