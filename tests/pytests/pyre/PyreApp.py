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

from pythia.pyre.applications.Script import Script
import pythia.pyre.inventory


from .TestComponents import (
    SimpleFacility,
    SimpleTooFacility,
    ComplexFacility,
    ArrayTwo,
    simpleFactory,
    VAULT,
)


class PyreApp(Script):

    from pythia.pyre.units.mass import kilogram

    DEFAULT_BOOLEAN = False
    DEFAULT_INT = 3
    DEFAULT_FLOAT = 4.5
    DEFAULT_STRING = "Hello World"
    DEFAULT_MASS = 2.0 * kilogram
    DEFAULT_LIST = ["a", "bb", "ccc"]
    DEFAULT_INTARRAY = [1, 2, 3]

    debug = pythia.pyre.inventory.bool("debug", default=False)
    valueBool = pythia.pyre.inventory.bool("value_boolean", default=DEFAULT_BOOLEAN)
    valueInt = pythia.pyre.inventory.int("value_int", default=DEFAULT_INT, validator=pythia.pyre.inventory.greater(0))
    valueFloat = pythia.pyre.inventory.float("value_float", default=DEFAULT_FLOAT, validator=pythia.pyre.inventory.greaterEqual(-1.0))
    valueString = pythia.pyre.inventory.str("value_string", default=DEFAULT_STRING)
    valueList = pythia.pyre.inventory.list("list_string", default=DEFAULT_LIST)
    valueIntArray = pythia.pyre.inventory.array("array_int", default=DEFAULT_INTARRAY, converter=int)
    valueMass = pythia.pyre.inventory.dimensional("value_mass", default=DEFAULT_MASS)
    fileIn = pythia.pyre.inventory.inputFile("input_file", default="stdin")
    fileOut = pythia.pyre.inventory.outputFile("output_file", default="stdout")

    facilitySimple = pythia.pyre.inventory.facility("simple_facility", family="simple", vault=VAULT, factory=SimpleFacility)
    facilityArray = pythia.pyre.inventory.facilityArray("facility_array", itemFactory=simpleFactory, factory=ArrayTwo)

    def __init__(self, name="pyreapp"):
        Script.__init__(self, name)

    def main(self, *args, **kwds):
        self.data = {
            "boolean": self.valueBool,
            "int": self.valueInt,
            "float": self.valueFloat,
            "string": self.valueString,
            "list": self.valueList,
            "array_int": self.valueIntArray,
            "file_in": self.fileIn,
            "file_out": self.fileOut,
            "mass": self.valueMass,
            "simple": self.facilitySimple.getData(),
            "array": [component.getData() for component in self.facilityArray.components()],
        }
        if self.debug:
            print(self.data)


if __name__ == "__main__":
    PyreApp().run()
