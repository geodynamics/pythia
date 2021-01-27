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

from .PyreApp import PyreApp

from .TestComponents import (
    SimpleFacility,
    SimpleTooFacility,
)
import unittest
import os


class TestInventory(unittest.TestCase):

    def test_defaults(self):
        app = PyreApp()
        app.run(argv=["pyreapp"])

        self.assertEqual(app.DEFAULT_BOOLEAN, app.data["boolean"])
        self.assertEqual(app.DEFAULT_INT, app.data["int"])
        self.assertEqual(app.DEFAULT_FLOAT, app.data["float"])
        self.assertEqual(app.DEFAULT_STRING, app.data["string"])
        self.assertEqual(app.DEFAULT_MASS, app.data["mass"])
        self.assertEqual(len(app.DEFAULT_LIST), len(app.data["list"]))
        for valueE, value in zip(app.DEFAULT_LIST, app.data["list"]):
            self.assertEqual(valueE, value)
        self.assertEqual(len(app.DEFAULT_INTARRAY), len(app.data["array_int"]))
        for valueE, value in zip(app.DEFAULT_INTARRAY, app.data["array_int"]):
            self.assertEqual(valueE, value)

        sdata = app.data["simple"]
        self.assertEqual(SimpleFacility.DEFAULT_INT, sdata["int"])
        self.assertEqual(SimpleFacility.DEFAULT_FLOAT, sdata["float"])
        self.assertEqual(SimpleFacility.DEFAULT_STRING, sdata["string"])

        adata = app.data["array"]
        self.assertEqual(2, len(adata))

        sdata = adata[0]
        self.assertEqual(SimpleFacility.DEFAULT_INT, sdata["int"])
        self.assertEqual(SimpleFacility.DEFAULT_FLOAT, sdata["float"])
        self.assertEqual(SimpleFacility.DEFAULT_STRING, sdata["string"])

        sdata = adata[1]
        self.assertEqual(SimpleFacility.DEFAULT_INT, sdata["int"])
        self.assertEqual(SimpleFacility.DEFAULT_FLOAT, sdata["float"])
        self.assertEqual(SimpleFacility.DEFAULT_STRING, sdata["string"])

    def test_commandline(self):
        app = PyreApp()
        args = [
            "--value_boolean=True",
            "--value_int=765",
            "--value_string=Hooray",
            "--list_string=[iii, jjj, kkk]",
            "--array_int=[6, 5, 4]",
            "--input_file=pyre/data.in",
            "--output_file=pyre/data.out",
            "--simple_facility=simpletoo-facility",
            "--facility_array.one.simple_int=34",
            "--facility_array.one.simple_string=one-one",
            "--facility_array.two.simple_int=56",
            "--facility_array.two.simple_string=two-two",
        ]
        app.run(argv=["pyreapp"] + args)

        self.assertEqual(True, app.data["boolean"])
        self.assertEqual(765, app.data["int"])
        self.assertEqual(app.DEFAULT_FLOAT, app.data["float"])
        self.assertEqual("Hooray", app.data["string"])
        self.assertEqual(app.DEFAULT_MASS, app.data["mass"])
        self.assertEqual(3, len(app.data["list"]))
        for valueE, value in zip(["iii", "jjj", "kkk"], app.data["list"]):
            self.assertEqual(valueE, value)
        self.assertEqual(3, len(app.data["array_int"]))
        for valueE, value in zip([6, 5, 4], app.data["array_int"]):
            self.assertEqual(valueE, value)

        sdata = app.data["simple"]
        self.assertEqual(SimpleTooFacility.DEFAULT_INT, sdata["int"])
        self.assertEqual(SimpleTooFacility.DEFAULT_FLOAT, sdata["float"])
        self.assertEqual(SimpleTooFacility.DEFAULT_STRING, sdata["string"])

        adata = app.data["array"]
        self.assertEqual(2, len(adata))

        sdata = adata[0]
        self.assertEqual(34, sdata["int"])
        self.assertEqual(SimpleFacility.DEFAULT_FLOAT, sdata["float"])
        self.assertEqual("one-one", sdata["string"])

        sdata = adata[1]
        self.assertEqual(56, sdata["int"])
        self.assertEqual(SimpleFacility.DEFAULT_FLOAT, sdata["float"])
        self.assertEqual("two-two", sdata["string"])

    def test_cfg(self):
        from pythia.pyre.units.mass import g

        app = PyreApp()
        app.run(argv=["pyreapp", "pyre/pyreapp_settings.cfg"])

        self.assertEqual(False, app.data["boolean"])
        self.assertEqual(83, app.data["int"])
        self.assertEqual(6.5, app.data["float"])
        self.assertEqual("Goodbye World", app.data["string"])
        self.assertEqual(5.0 * g, app.data["mass"])
        self.assertEqual(4, len(app.data["list"]))
        for valueE, value in zip(["d", "e", "f", "g"], app.data["list"]):
            self.assertEqual(valueE, value)
        self.assertEqual(3, len(app.data["array_int"]))
        for valueE, value in zip([7, 8, 9], app.data["array_int"]):
            self.assertEqual(valueE, value)

        sdata = app.data["simple"]
        self.assertEqual(11, sdata["int"])
        self.assertEqual(-0.1, sdata["float"])
        self.assertEqual("Hello", sdata["string"])

        adata = app.data["array"]
        self.assertEqual(3, len(adata))

        sdata = adata[0]
        self.assertEqual(4, sdata["int"])
        self.assertEqual(4.4, sdata["float"])
        self.assertEqual("fore", sdata["string"])

        cdata = adata[1]
        self.assertEqual(5, cdata["int"])
        self.assertEqual(5.5, cdata["float"])
        self.assertEqual("jive", cdata["string"])
        sdata = cdata["facility"]
        self.assertEqual(55, sdata["int"])
        self.assertEqual(55.5, sdata["float"])
        self.assertEqual("jive five", sdata["string"])

        sdata = adata[2]
        self.assertEqual(6, sdata["int"])
        self.assertEqual(6.6, sdata["float"])
        self.assertEqual("sixty", sdata["string"])

    def test_pml(self):
        from pythia.pyre.units.mass import kg

        app = PyreApp()
        app.run(argv=["pyreapp", "pyre/pyreapp_settings.pml"])

        self.assertEqual(False, app.data["boolean"])
        self.assertEqual(82, app.data["int"])
        self.assertEqual(5.6, app.data["float"])
        self.assertEqual("Goodbye!", app.data["string"])
        self.assertEqual(5.0 * kg, app.data["mass"])
        self.assertEqual(4, len(app.data["list"]))
        for valueE, value in zip(["kk", "ll", "mm", "oo"], app.data["list"]):
            self.assertEqual(valueE, value)
        self.assertEqual(2, len(app.data["array_int"]))
        for valueE, value in zip([7, 4], app.data["array_int"]):
            self.assertEqual(valueE, value)

        sdata = app.data["simple"]
        self.assertEqual(12, sdata["int"])
        self.assertEqual(-0.2, sdata["float"])
        self.assertEqual("heLLo", sdata["string"])

    def test_pcs(self):
        from pythia.pyre.units.mass import g

        app = PyreApp()
        app.run(argv=["pyreapp", "pyre/pyreapp_settings.pcs"])

        self.assertEqual(False, app.data["boolean"])
        self.assertEqual(83, app.data["int"])
        self.assertEqual(6.5, app.data["float"])
        self.assertEqual("Goodbye World", app.data["string"])
        self.assertEqual(5.0 * g, app.data["mass"])
        self.assertEqual(3, len(app.data["list"]))
        for valueE, value in zip(["a", "bb", "ccc"], app.data["list"]):
            self.assertEqual(valueE, value)
        self.assertEqual(3, len(app.data["array_int"]))
        for valueE, value in zip([1, 2, 3], app.data["array_int"]):
            self.assertEqual(valueE, value)

        sdata = app.data["simple"]
        self.assertEqual(11, sdata["int"])
        self.assertEqual(-0.1, sdata["float"])
        self.assertEqual("Hello", sdata["string"])

        sdata = app.data["array"][0]
        self.assertEqual(1, sdata["int"])
        self.assertEqual(1.4, sdata["float"])
        self.assertEqual("one fore", sdata["string"])

        sdata = app.data["array"][1]
        self.assertEqual(2, sdata["int"])
        self.assertEqual(2.4, sdata["float"])
        self.assertEqual("two fore", sdata["string"])


def test_classes():
    return [TestInventory]


if __name__ == "__main__":
    suite = unittest.TestSuite()
    for cls in test_classes():
        suite.addTest(unittest.makeSuite(cls))
    unittest.TextTestRunner(verbosity=2).run(suite)


# End of file
