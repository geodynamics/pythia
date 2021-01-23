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


def run():
    import pythia.journal.services

    app = pythia.journal.services.daemon()
    return app.run(spawn=True)


if __name__ == "__main__":
    run()


# version
__id__ = "$Id: pythia.journald.py,v 1.1 2005/03/14 05:48:18 aivazis Exp $"

# End of file
