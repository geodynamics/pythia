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

from pythia.pyre.components.Component import Component
import pythia.pyre.inventory

VAULT = ["./pyre"]


class SimpleFacility(Component):

    DEFAULT_INT = 7
    DEFAULT_FLOAT = 8.0
    DEFAULT_STRING = "Goodbye"

    valueInt = pythia.pyre.inventory.int("simple_int", default=DEFAULT_INT, validator=pythia.pyre.inventory.isBoth(
        pythia.pyre.inventory.greaterEqual(0), pythia.pyre.inventory.less(100)))
    valueFloat = pythia.pyre.inventory.float("simple_float", default=DEFAULT_FLOAT)
    valueString = pythia.pyre.inventory.str("simple_string", default=DEFAULT_STRING)

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

    nonzero = pythia.pyre.inventory.isEither(pythia.pyre.inventory.greater(0), pythia.pyre.inventory.less(0))
    valueInt = pythia.pyre.inventory.int("too_int", default=DEFAULT_INT, validator=nonzero)
    valueFloat = pythia.pyre.inventory.float("too_float", default=DEFAULT_FLOAT, validator=pythia.pyre.inventory.range(0.0, 200.0))
    valueString = pythia.pyre.inventory.str("too_string", default=DEFAULT_STRING)

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

    valueInt = pythia.pyre.inventory.int("complex_int", default=DEFAULT_INT, validator=pythia.pyre.inventory.lessEqual(20))
    valueFloat = pythia.pyre.inventory.float("complex_float", default=DEFAULT_FLOAT)
    valueString = pythia.pyre.inventory.str("complex_string", default=DEFAULT_STRING)
    nestedFacility = pythia.pyre.inventory.facility("complex_facility", family="simple", factory=SimpleFacility)

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

    one = pythia.pyre.inventory.facility("one", family="simple", vault=VAULT, factory=SimpleFacility)
    two = pythia.pyre.inventory.facility("two", family="simple", vault=VAULT, factory=SimpleFacility)

    def __init__(self, name="arraytwo"):
        Component.__init__(self, name, facility="simple")

    def components(self):
        return [self.one, self.two]


def simpleFactory(name):
    return pythia.pyre.inventory.facility(name, family="simple", vault=VAULT, factory=SimpleFacility)


# End of file
