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


from pythia.pyre.inventory.Facility import Facility


class FacilityArrayFacility(Facility):

    def __init__(self, name, itemFactory, **kwds):
        Facility.__init__(self, name=name, **kwds)
        self.itemFactory = itemFactory
        return

    def _retrieveComponent(self, instance, componentName):
        facilityNames = self._cast(componentName)

        facilityOrder = []
        dict = {}
        for index, facilityName in enumerate(facilityNames):
            # Strip leading and trailing whitespace from facility name
            facility = self.itemFactory(facilityName.strip())
            attr = "item%05d" % index
            dict[attr] = facility
            facilityOrder.append(facilityName.strip())

        from .Inventory import Inventory
        from pythia.pyre.components.Component import Component
        Inventory = type(Inventory)("FacilityArray.Inventory", (Component.Inventory,), dict)

        dict = {'Inventory': Inventory}
        FacilityArray = type(Component)("FacilityArray", (Component,), dict)
        fa = FacilityArray(self.name)
        fa.Inventory._facilityOrder = facilityOrder

        import pythia.pyre.parsing.locators
        locator = pythia.pyre.parsing.locators.builtIn()

        return fa, locator

    def _cast(self, text):
        if isinstance(text, str):
            if text and text[0] in '[({':
                text = text[1:]
            if text and text[-1] in '])}':
                text = text[:-1]

            value = text.split(",")

            # allow trailing comma
            if len(value) and not value[-1]:
                value.pop()
        else:
            value = text

        if isinstance(value, list):
            return value

        raise TypeError("facility '%s': could not convert '%s' to a list" % (self.name, text))


# end of file
