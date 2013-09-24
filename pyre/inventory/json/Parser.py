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

from pyre.util import expandMacros
import pyre.parsing.locators as locators

class Parser(object):
    """
    Use json parser to get data and then populate Pyre Registry.
    """

    def __init__(self, name):
        """
        Constructor.
        """
        self.name = name
        return


    def read(self):
        """
        Parse json and populate registry.
        """
        import json
        jdata = json.load(file(self.name))

        from pyre.inventory.odb.Registry import Registry
        root = Registry("root")

        # :KLUDGE: Would have to reimplement json scanner to get line
        # number. Set the filename correctly in the locator, but use a
        # line number of -1.
        self.locatorNL = locators.file(self.name, -1)

        self._setNode(root, jdata)
        return root


    def _setNode(self, node, jdata):
        """
        Set registry data for node from json data.
        """
        if not isinstance(jdata, dict):
            raise ValueError("Dictionary expected. Object: %s" % jdata)

        for (key, value) in jdata.items():
            if isinstance(value, dict): # facility or dimensional
                if value.has_key("value") and value.has_key("units"): # dimensional
                    node.setProperty(key, "%s*%s" % (value['value'], value['units']), self.locatorNL)
                else: # facility
                    module = value.pop('_module', None)
                    if module is None:
                        raise ValueError("Component missing '_module' key. Object: %s" % value)
                    node.setProperty(key, module, self.locatorNL)
                    facility = node.getNode(key)
                    self._setNode(facility, value)

            elif isinstance(value, list): # facility array
                facilityArray = node.getNode(key)
                for item in value:
                    if not isinstance(item, dict):
                        raise ValueError("Expected dictionaries in facility array '%s'. Object: %s" % \
                                             (value, item))
                    if not item.has_key('_value') or not item.has_key('_item'):
                        raise ValueError("Expected facility array dictionary to contain '_value' and '_item' keys. Object: %s" % item)
                    module = item['_value'].pop('_module', None)
                    if module is None:
                        raise ValueError("Component '%s' missing '_module' key." % item['_value'])
                    facilityArray.setProperty(item['_item'], module, self.locatorNL)
                    facility = facilityArray.getNode(item['_item'])
                    self._setNode(facility, item['_value'])

            else: # property
                node.setProperty(key, value, self.locatorNL)
              
        return


# End of file
