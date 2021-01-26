#!/usr/bin/env python
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

import step01_facility
import step02_facilityvault
import step03_facilityarray


def run_app(app, args=[]):
    print("Running '{}' with args={} ...".format(app.__doc__, args))
    app.run(argv=[app.name] + args)
    print("Finished running '{}'.\n".format(app.__doc__))


def run_step01():
    app = step01_facility.GreeterApp()
    run_app(app)
    run_app(app, args=["--greeter.greeting=Howdy there"])
    run_app(app, args=["--greeter=greeters.Alien"])
    run_app(app, args=["step01_human.cfg"])


def run_step02():
    app = step02_facilityvault.GreeterApp()
    run_app(app)
    run_app(app, args=["--greeter=robot"])
    run_app(app, args=["--greeter=robot", "--robot.model=RPT56"])
    run_app(app, args=["step02_robot.cfg"])


def run_step03():
    app = step03_facilityarray.GreeterApp()
    run_app(app)
    run_app(app, args=["--greeters.left=greeters.Human"])
    run_app(app, args=["--greeters.right=remotehuman"])
    run_app(app, args=["step03_leftright.cfg"])
    run_app(app, args=["step03_three.cfg"])


def run():
    run_step01()
    run_step02()
    run_step03()


if __name__ == "__main__":
    run()
