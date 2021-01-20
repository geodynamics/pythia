#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                             Michael A.G. Aivazis
#                      California Institute of Technology
#                      (C) 1998-2005  All Rights Reserved
#
# <LicenseText>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

import journal


def logfile(stream):
    from .File import File
    device = File(stream)

    journal.journal().device = device
    return device


def remote(key, port, host="localhost", protocol="tcp"):

    if protocol == "tcp":
        from .TCPDevice import TCPDevice
        device = TCPDevice(key, port, host)
    elif protocol == "udp":
        from .UDPDevice import UDPDevice
        device = UDPDevice(key, port, host)
    else:
        import journal.diagnostics
        journal.diagnostics.error('journal').log("unknown protocol '%s'" % protocol)
        return

    journal.journal().device = device
    return device


# End of file
