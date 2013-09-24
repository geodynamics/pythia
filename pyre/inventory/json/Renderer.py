#!/usr/bin/env python
#
# ----------------------------------------------------------------------
#
# Brad T. Aagaard, U.S. Geological Survey
#
# This code was developed as part of the Computational Infrastructure
# for Geodynamics (http://geodynamics.org).
#
# Copyright (c) 2010-2013 University of California, Davis
#
# ----------------------------------------------------------------------


from pyre.weaver.mills.ConfigMill import ConfigMill


class Renderer(ConfigMill):


    def render(self, inventory):
        raise NotImplementedError("Renering json files not implemented.")
        retun


    # handlers

    def onInventory(self, inventory):
        raise NotImplementedError("Renering json files not implemented.")
        return

    
    def onRegistry(self, registry):
        raise NotImplementedError("Renering json files not implemented.")
        return


    def __init__(self):
        ConfigMill.__init__(self)
        self.path = []
        return


    def _renderDocument(self, document):
        return document.identify(self)


# end of file
