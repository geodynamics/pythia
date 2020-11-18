# ======================================================================
#
# Brad T. Aagaard, U.S. Geological Survey
#
# This code was developed as part of the Computational Infrastructure
# for Geodynamics (http://geodynamics.org).
#
# Copyright (c) 2010-2017 University of California, Davis
#
# See COPYING for license information.
#
# ======================================================================
#

from pyre.components.Component import Component
import pyre.inventory

VAULT = ["tests/pyre/test_vault"]


class SimpleFacility(Component):

    DEFAULT_INT = 7
    DEFAULT_FLOAT = 8.0
    DEFAULT_STRING = "Goodbye"

    valueInt = pyre.inventory.int("simple_int", default=DEFAULT_INT, validator=pyre.inventory.isBoth(
        pyre.inventory.greaterEqual(0), pyre.inventory.less(100)))
    valueFloat = pyre.inventory.float("simple_float", default=DEFAULT_FLOAT)
    valueString = pyre.inventory.str("simple_string", default=DEFAULT_STRING)

    def __init__(self, name="simplefacility"):
        Component.__init__(self, name, facility="simple")

    def getData(self):
        return {
            "int": self.valueInt,
            "float": self.valueFloat,
            "string": self.valueString,
        }


class SimpleTooFacility(Component):

    DEFAULT_INT = 23
    DEFAULT_FLOAT = 24.0
    DEFAULT_STRING = "Welcome"

    nonzero = pyre.inventory.isEither(pyre.inventory.greater(0), pyre.inventory.less(0))
    valueInt = pyre.inventory.int("too_int", default=DEFAULT_INT, validator=nonzero)
    valueFloat = pyre.inventory.float("too_float", default=DEFAULT_FLOAT, validator=pyre.inventory.range(0.0, 200.0))
    valueString = pyre.inventory.str("too_string", default=DEFAULT_STRING)

    def __init__(self, name="simpletoofacility"):
        Component.__init__(self, name, facility="simple")

    def getData(self):
        return {
            "int": self.valueInt,
            "float": self.valueFloat,
            "string": self.valueString,
        }


class ComplexFacility(Component):

    DEFAULT_INT = 12
    DEFAULT_FLOAT = 20.0
    DEFAULT_STRING = "Howdy"

    valueInt = pyre.inventory.int("complex_int", default=DEFAULT_INT, validator=pyre.inventory.lessEqual(20))
    valueFloat = pyre.inventory.float("complex_float", default=DEFAULT_FLOAT)
    valueString = pyre.inventory.str("complex_string", default=DEFAULT_STRING)
    nestedFacility = pyre.inventory.facility("complex_facility", family="simple", factory=SimpleFacility)

    def __init__(self, name="complexfacility"):
        Component.__init__(self, name, facility="complex")

    def getData(self):
        return {
            "int": self.valueInt,
            "float": self.valueFloat,
            "string": self.valueString,
            "facility": self.nestedFacility.getData(),
        }


class ArrayTwo(Component):

    one = pyre.inventory.facility("one", family="simple", vault=VAULT, factory=SimpleFacility)
    two = pyre.inventory.facility("two", family="simple", vault=VAULT, factory=SimpleFacility)

    def __init__(self, name="arraytwo"):
        Component.__init__(self, name, facility="simple")

    def components(self):
        return [self.one, self.two]


def simpleFactory(name):
    return pyre.inventory.facility(name, family="simple", vault=VAULT, factory=SimpleFacility)


# End of file
