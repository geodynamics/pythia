#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                             Michael A.G. Aivazis
#                      California Institute of Technology
#                      (C) 1998-2005  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#



from .Trait import Trait
from .Facility import Facility


class Notary(type):


    def __init__(cls, name, bases, dict):
        type.__init__(cls, name, bases, dict)

        traitRegistry = {}
        facilityRegistry = {}
        myTraitRegistry = {}

        # register inherited traits
        bases = list(bases)
        bases.reverse()
        for base in bases:
            try:
                traitRegistry.update(base._traitRegistry)
            except AttributeError:
                pass

            try:
                facilityRegistry.update(base._facilityRegistry)
            except AttributeError:
                pass

        # scan the class record for traits
        for name, item in cls.__dict__.items():

            # disregard entries that do not derive from Trait
            if not isinstance(item, Trait):
                continue

            item.attr = name
            # set the public name of trait if it is not set already
            if item.name is None:
                item.name = name

            # register it
            traitRegistry[item.name] = item
            myTraitRegistry[item.name] = item

            # facilities also go into their own bucket
            if isinstance(item, Facility):
                facilityRegistry[item.name] = item
            
        # install the registries into the class record
        cls._traitRegistry = traitRegistry
        cls._facilityRegistry = facilityRegistry
        cls._myTraitRegistry = myTraitRegistry

        return


# version
__id__ = "$Id: Notary.py,v 1.1.1.1 2005/03/08 16:13:43 aivazis Exp $"

# End of file 
