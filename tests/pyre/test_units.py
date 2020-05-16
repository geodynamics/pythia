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

import unittest
from math import pi

import pyre.units.SI as SI
import pyre.units.unit as unit

class TestUnits(unittest.TestCase):

    def test_SI(self):
        self.assertEqual(1.0e+24, SI.yotta)
        self.assertEqual(1.0e+21, SI.zetta)
        self.assertEqual(1.0e+18, SI.exa)
        self.assertEqual(1.0e+15, SI.peta)
        self.assertEqual(1.0e+12, SI.tera)
        self.assertEqual(1.0e+9, SI.giga)
        self.assertEqual(1.0e+6, SI.mega)
        self.assertEqual(1.0e+3, SI.kilo)
        self.assertEqual(1.0e+2, SI.hecto)
        self.assertEqual(1.0e+1, SI.deka)
        self.assertEqual(1.0e-1, SI.deci)
        self.assertEqual(1.0e-2, SI.centi)
        self.assertEqual(1.0e-3, SI.milli)
        self.assertEqual(1.0e-6, SI.micro)
        self.assertEqual(1.0e-9, SI.nano)
        self.assertEqual(1.0e-12, SI.pico)
        self.assertEqual(1.0e-15, SI.femto)
        self.assertEqual(1.0e-18, SI.atto)
        self.assertEqual(1.0e-21, SI.zepto)
        self.assertEqual(1.0e-24, SI.yocto)
        
        self.assertEqual(1.0, SI.meter.value)
        self.assertEqual(1.0, SI.kilogram.value)
        self.assertEqual(1.0, SI.second.value)
        self.assertEqual(1.0, SI.ampere.value)
        self.assertEqual(1.0, SI.kelvin.value)
        self.assertEqual(1.0, SI.mole.value)
        
        self.assertEqual(1.0/SI.second, SI.hertz)
        self.assertEqual(SI.meter*SI.kilogram/SI.second**2, SI.newton)
        self.assertEqual(SI.newton/SI.meter**2, SI.pascal)
        self.assertEqual(SI.newton*SI.meter, SI.joule)
        self.assertEqual(SI.joule/SI.second, SI.watt)
        self.assertEqual(SI.ampere*SI.second, SI.coulomb)
        self.assertEqual(SI.watt/SI.ampere, SI.volt)
        self.assertEqual(SI.coulomb/SI.volt, SI.farad)
        self.assertEqual(SI.volt/SI.ampere, SI.ohm)
        self.assertEqual(SI.ampere/SI.volt, SI.siemens)
        self.assertEqual(SI.volt*SI.second, SI.weber)
        self.assertEqual(SI.weber/SI.meter**2, SI.tesla)
        self.assertEqual(SI.weber/SI.ampere, SI.henry)
        self.assertEqual(SI.kelvin, SI.celcius)

        self.assertEqual(2**10, SI.kibi)
        self.assertEqual(SI.kibi**2, SI.mebi)
        self.assertEqual(SI.kibi**3, SI.gibi)
        self.assertEqual(SI.kibi**4, SI.tebi)
        self.assertEqual(SI.kibi**5, SI.pebi)
        self.assertEqual(SI.kibi**6, SI.exbi)

    def test_angle(self):
        import pyre.units.angle as angle
        self.assertEqual(pi/180.0, angle.degree.value)
        self.assertEqual(angle.degree, angle.deg)
        self.assertEqual(angle.degree/60.0, angle.arcminute)
        self.assertEqual(angle.degree/(60.0*60.0), angle.arcsecond)
        self.assertEqual(SI.radian, angle.rad)

    def test_area(self):
        import pyre.units.area as area
        from pyre.units.length import meter, centimeter, foot, inch, mile
        self.assertEqual(meter**2, area.square_meter)
        self.assertEqual(centimeter**2, area.square_centimeter)
        self.assertEqual(foot**2, area.square_foot)
        self.assertEqual(inch**2, area.square_inch)
        self.assertEqual(mile**2, area.square_mile)

    def test_density(self):
        import pyre.units.density as density
        from pyre.units.mass import kilogram
        from pyre.units.length import meter
        self.assertEqual(kilogram/meter**3, density.kg/density.meter**3)

    def test_energy(self):
        import pyre.units.energy as energy
        self.assertEqual(1.0e-7*SI.joule, energy.erg)
        self.assertEqual(4.1858*SI.joule, energy.calorie)
        self.assertEqual(4.1858e+3*SI.joule, energy.Calorie)
        self.assertEqual(3.6e+6*SI.joule, energy.kilowatt_hour)
        self.assertEqual(1.356*SI.joule, energy.foot_pound)
        self.assertEqual(SI.joule, energy.J)
        self.assertEqual(1.0e+3*SI.joule, energy.kJ)
        self.assertEqual(1.0e+6*SI.joule, energy.MJ)
        self.assertEqual(energy.calorie, energy.cal)
        self.assertEqual(1.0e+3*energy.calorie, energy.kcal)

    def test_force(self):
        import pyre.units.force as force
        self.assertEqual(0.01*SI.meter/SI.second**2, force.gal)

    def test_length(self):
        import pyre.units.length as length
        self.assertEqual(SI.nano*SI.meter, length.nanometer)
        self.assertEqual(SI.micro*SI.meter, length.micrometer)
        self.assertEqual(SI.milli*SI.meter, length.millimeter)
        self.assertEqual(SI.centi*SI.meter, length.centimeter)
        self.assertEqual(SI.kilo*SI.meter, length.kilometer)
        self.assertEqual(SI.meter, length.m)
        self.assertEqual(SI.nano*SI.meter, length.nm)
        self.assertEqual(SI.micro*SI.meter, length.um)
        self.assertEqual(SI.micro*SI.meter, length.micron)
        self.assertEqual(SI.milli*SI.meter, length.mm)
        self.assertEqual(SI.centi*SI.meter, length.cm)
        self.assertEqual(SI.kilo*SI.meter, length.km)
        self.assertEqual(2.54*length.cm, length.inch)
        self.assertEqual(12*length.inch, length.foot)
        self.assertEqual(3*length.foot, length.yard)
        self.assertEqual(5280*length.foot, length.mile)
        self.assertEqual(6*length.foot, length.fathom)
        self.assertEqual(1852*SI.meter, length.nautical_mile)
        
    def test_mass(self):
        import pyre.units.mass as mass
        self.assertEqual(SI.kilogram/SI.kilo, mass.gram)
        self.assertEqual(SI.centi*mass.gram, mass.centigram)
        self.assertEqual(SI.milli*mass.gram, mass.milligram)
        self.assertEqual(SI.kilogram, mass.kg)
        self.assertEqual(mass.gram, mass.g)
        self.assertEqual(mass.centigram, mass.cg)
        self.assertEqual(mass.milligram, mass.mg)
        self.assertEqual(1000*SI.kilogram, mass.metric_ton)
        self.assertEqual(28.35*mass.gram, mass.ounce)
        self.assertEqual(16*mass.ounce, mass.pound)
        self.assertEqual(2000*mass.pound, mass.ton)

    def test_power(self):
        import pyre.units.power as power
        self.assertEqual(SI.kilo*SI.watt, power.kilowatt)
        self.assertEqual(745.7*SI.watt, power.horsepower)

    def test_pressure(self):
        import pyre.units.pressure as pressure
        self.assertEqual(SI.pascal, pressure.Pa)
        self.assertEqual(SI.kilo*SI.pascal, pressure.kPa)
        self.assertEqual(SI.mega*SI.pascal, pressure.MPa)
        self.assertEqual(SI.giga*SI.pascal, pressure.GPa)
        self.assertEqual(1.0e+5*SI.pascal, pressure.bar)
        self.assertEqual(SI.milli*pressure.bar, pressure.millibar)
        self.assertEqual(133.3*SI.pascal, pressure.torr)
        self.assertEqual(101325*SI.pascal, pressure.atmosphere)
        self.assertEqual(pressure.atmosphere, pressure.atm)
        
    def test_speed(self):
        import pyre.units.speed as speed
        from pyre.units.time import hour
        from pyre.units.length import nautical_mile
        self.assertEqual(nautical_mile/hour, speed.knot)

    def test_substance(self):
        import pyre.units.substance as substance
        self.assertEqual(SI.mole, substance.mol)
        self.assertEqual(SI.kilo*SI.mole, substance.kmol)

    def test_temperature(self):
        import pyre.units.temperature as temperature
        self.assertEqual(SI.kelvin, temperature.K)

    def test_time(self):
        import pyre.units.time as time
        self.assertEqual(SI.pico*SI.second, time.picosecond)
        self.assertEqual(SI.nano*SI.second, time.nanosecond)
        self.assertEqual(SI.micro*SI.second, time.microsecond)
        self.assertEqual(SI.milli*SI.second, time.millisecond)
        self.assertEqual(SI.second, time.s)
        self.assertEqual(time.picosecond, time.ps)
        self.assertEqual(time.nanosecond, time.ns)
        self.assertEqual(time.microsecond, time.us)
        self.assertEqual(time.millisecond, time.ms)
        self.assertEqual(60*SI.second, time.minute)
        self.assertEqual(60*time.minute, time.hour)
        self.assertEqual(24*time.hour, time.day)
        self.assertEqual(365.25*time.day, time.year)
        
    def test_volume(self):
        import pyre.units.volume as volume
        from pyre.units.length import centimeter, foot, inch
        self.assertEqual(SI.meter**3, volume.cubic_meter)
        self.assertEqual(centimeter**3, volume.cubic_centimeter)
        self.assertEqual(foot**3, volume.cubic_foot)
        self.assertEqual(inch**3, volume.cubic_inch)
        self.assertEqual(1000*volume.cubic_centimeter, volume.liter)
        self.assertEqual(231.0/128.0*volume.cubic_inch, volume.us_fluid_ounce)
        self.assertEqual(16*volume.us_fluid_ounce, volume.us_pint)
        self.assertEqual(2*volume.us_pint, volume.us_fluid_quart)
        self.assertEqual(4*volume.us_fluid_quart, volume.us_fluid_gallon)

    def test_parser(self):
        import pyre.units
        parser = pyre.units.parser()
        self.assertEqual(1.0, parser.parse("1.0"))
        self.assertEqual(2.0*SI.meter, parser.parse("2.0*meter"))
        self.assertEqual(3.0*SI.kilogram, parser.parse("3.0*kilogram"))
        self.assertEqual(5*SI.second, parser.parse("5*second"))
        self.assertEqual(100*SI.kelvin, parser.parse("100*kelvin"))
        self.assertEqual(100*SI.pascal, parser.parse("100*Pa"))
        
        self.assertEqual(2.0*SI.meter/SI.second, parser.parse("2.0*meter/second"))
        self.assertEqual(2.0*SI.kilogram/SI.meter**3, parser.parse("2.0*kg/m**3"))
        self.assertEqual(6.0e+6*SI.pascal*SI.second, parser.parse("6.0*MPa*s"))


class TestUnit(unittest.TestCase):

    def test_init(self):
        value = 1.0
        derivation = (1, 2, 3, 4, 5, 6, 7)
        quantity = unit.unit(value, derivation)
        self.assertEqual(value,quantity.value)
        self.assertEqual(len(derivation), len(quantity.derivation))
        for dE, d in zip(derivation, quantity.derivation):
            self.assertEqual(dE, d)

    def test_add(self):
        self.assertEqual(5.0*SI.meter, 2.0*SI.meter + 3.0*SI.meter)
        self.assertEqual(3.0*SI.meter/SI.second, 1.0*SI.meter/SI.second + 2.0*SI.meter/SI.second)
        self.assertEqual(22.0*SI.mega*SI.pascal, 15.0e+6*SI.pascal + 7.0*SI.mega*SI.pascal)

        with self.assertRaises(unit.IncompatibleUnits):
            x = 1.0*SI.meter + 1.0*SI.second
        
    def test_subtract(self):
        self.assertEqual(-1.0*SI.meter, 2.0*SI.meter - 3.0*SI.meter)
        self.assertEqual(3.0*SI.meter/SI.second, 4.0*SI.meter/SI.second - 1.0*SI.meter/SI.second)
        self.assertEqual(8.0*SI.mega*SI.pascal, 15.0e+6*SI.pascal - 7.0*SI.mega*SI.pascal)

        with self.assertRaises(unit.IncompatibleUnits):
            x = 1.0*SI.meter - 1.0*SI.second

    def test_multiply(self):
        self.assertEqual(6.0*SI.meter*SI.second, 2.0*SI.meter * 3.0*SI.second)
        self.assertEqual(2.0*SI.meter/SI.second, 1.0*SI.meter/SI.second * 2.0*SI.meter/SI.second)
        self.assertEqual(105.0*SI.mega*SI.pascal, 15.0*SI.pascal * 7.0*SI.mega)
        self.assertEqual(105.0*SI.mega*SI.pascal, 15.0 * 7.0*SI.mega*SI.pascal)
        self.assertEqual(105.0*SI.mega*SI.pascal, 15.0*SI.mega*SI.pascal * 7.0)
        self.assertEqual(105.0*SI.mega, 15.0 * 7.0*SI.mega)
        
    def test_divide(self):
        self.assertEqual(4.0*SI.meter, (8.0*SI.meter/SI.second) / 2.0*SI.meter)
        self.assertEqual(3.0, (15.0*SI.meter/SI.second) / (5.0*SI.meter/SI.second))
        self.assertEqual(15.0*SI.pascal, 105.0e+6*SI.pascal / (7.0*SI.mega))
        self.assertEqual(15.0*SI.pascal, 105.0*SI.pascal / 7.0)
        self.assertEqual(15.0/SI.meter, 105.0 / (7.0*SI.meter))

    def test_power(self):
        self.assertEqual(5.0*SI.meter*SI.meter, 5.0*SI.meter**2)
        self.assertEqual(3.0/(SI.second*SI.second), 3.0*SI.meter**-2)
        self.assertEqual(15.0*SI.pascal, 15.0e+6*SI.pascal*SI.mega**-1)

        with self.assertRaises(unit.InvalidOperation):
            x = 2.0*SI.meter**"abc"

    def test_positive(self):
        self.assertEqual(5.0*SI.meter, +5.0*SI.meter)
        self.assertEqual(3.0*SI.meter/SI.second, +3.0*SI.meter/SI.second)
        self.assertEqual(15.0*SI.mega*SI.pascal, +15.0*SI.mega*SI.pascal)

    def test_negative(self):
        self.assertEqual(-5.0, (-5.0*SI.meter).value)
        self.assertEqual(-3.0, (-3.0*SI.meter/SI.second).value)
        self.assertEqual(-1.5e+7, (-15.0*SI.mega*SI.pascal).value)

    def test_abs(self):
        self.assertEqual(5.0*SI.meter, abs(5.0*SI.meter))
        self.assertEqual(3.0*SI.meter/SI.second, abs(-3.0*SI.meter/SI.second))
        self.assertEqual(15.0*SI.mega*SI.pascal, abs(-15.0*SI.mega*SI.pascal))

    def test_invert(self):
        import operator
        self.assertEqual(0.2/SI.meter, operator.invert(5.0*SI.meter))
        self.assertEqual(-1025, ~SI.kibi)
        self.assertEqual(-2*SI.meter, ~1*SI.meter)

    def test_cmp(self):
        self.assertTrue(5.0*SI.meter == 2.0*SI.meter + 3.0*SI.meter)
        self.assertTrue(3.0*SI.meter/SI.second == 1.0*SI.meter/SI.second + 2.0*SI.meter/SI.second)
        self.assertTrue(22.0*SI.mega*SI.pascal == 15.0e+6*SI.pascal + 7.0*SI.mega*SI.pascal)
        self.assertTrue(1.0*SI.meter == 1.0*SI.second)
        self.assertFalse(1.0*SI.meter == 2.0*SI.meter)

    def test_str(self):
        self.assertEqual("5*m", str(5.0*SI.meter))
        self.assertEqual("3*s", str(3.0*SI.second))
        self.assertEqual("3", str(unit.unit(3, unit.unit._zero)))
        self.assertEqual("2.2e+07*m**-1*kg*s**-2", str(22.0*SI.mega*SI.pascal))

    def test_repr(self):
        self.assertEqual("5*m", repr(5.0*SI.meter))
        self.assertEqual("3*s", repr(3.0*SI.second))
        self.assertEqual("3", repr(unit.unit(3, unit.unit._zero)))
        self.assertEqual("2.2e+07*m**-1*kg*s**-2", repr(22.0*SI.mega*SI.pascal))


    def test_float(self):
        self.assertEqual(4.0e+3, float(4.0*SI.kilo))

        with self.assertRaises(unit.InvalidConversion):
            x = float(3.0*SI.meter)

    def test_exceptions(self):
        value = unit.unit(3, unit.unit._zero)
        
        x = str(unit.InvalidConversion(value))
        x = str(unit.InvalidOperation("*", value, value))
        x = str(unit.IncompatibleUnits("*", value, value))


# End of file
