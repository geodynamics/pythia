#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                      California Institute of Technology
#                        (C) 2006  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

import itertools

from configparser import ConfigParser
import pythia.pyre.parsing.locators as locators
from pythia.pyre.util import expandMacros


class Parser(ConfigParser):
    """Python's ConfigParser, hacked to provide file & line info, and extended to populate a Pyre Registry.

    The dictionary is created for compatibility with ConfigParser. We use the Pyre Registry. 
    """

    # This class goes to extreme lengths to extract file and line info
    # from Python's ConfigParser module.  It injects proxy 'file' and
    # 'dict' objects into ConfigParser's code.  As the file is parsed,
    # the proxy objects gain control, spying upon the parsing process.

    # We should probably write our own parser... *sigh*

    class FileProxy(object):

        def __init__(self):
            self.fp = None
            self.name = "unknown"
            self.lineno = 0

        def __iter__(self):
            line = self.fp.readline()
            while line:
                self.lineno += 1
                yield line
                line = self.fp.readline()

        def __getattr__(self, name):
            return getattr(self.fp, name)

    class Section(dict):

        def __init__(self, sectname, node, macros, fp):
            dict.__init__(self)
            self.node = node
            self.macros = macros
            self.fp = fp
            self.locators = {}

        def __setitem__(self, trait, value):
            locator = locators.file(self.fp.name, self.fp.lineno)
            path = trait.split('.')
            key = path[-1]
            path = path[:-1]
            node = _getNode(self.node, path)

            # In the initial pass, everything comes in as a list. We save the locator because when
            # the lists are removed in the second pass, the locator will be at the end of the file.
            # In the first pass we store the value in the dictionry using the trait and then get
            # the correct node in the registry in the second pass.
            if isinstance(value, list):
                assert(1 == len(value))
                self.locators[trait] = locator
                dict.__setitem__(self, trait, value)
            else:
                value = expandMacros(value, self.macros)
                node.setProperty(key, value, self.locators[trait])

    class SectionDict(dict):

        def __init__(self, root, macros):
            dict.__init__(self)
            self.root = root
            self.macros = macros
            self.fp = Parser.FileProxy()

        def __contains__(self, sectname):
            # Prevent 'ConfigParser' from creating section
            # dictionaries; instead, create our own.
            if not dict.__contains__(self, sectname):
                node = _getNode(self.root, sectname.split('.'))
                cursect = Parser.Section(sectname, node, self.macros, self.fp)
                self[sectname] = cursect
            return True

        def __setitem__(self, key, value):
            dict.__setitem__(self, key, value)

    def __init__(self, root, defaults=None, macros=None):
        ConfigParser.__init__(
            self, defaults, empty_lines_in_values=False, strict=False)
        if macros is None:
            macros = dict()
        self._sections = Parser.SectionDict(root, macros)

    def _read(self, fp, fpname):
        self._sections.fp.fp = fp
        self._sections.fp.name = fpname
        self._sections.fp.lineno = 0
        ConfigParser._read(self, self._sections.fp, fpname)
        self._sections.fp.__init__()

    def optionxform(self, optionstr):
        # Don't lower() option names.
        return optionstr

    def _join_multiline_values(self):
        defaults = self.default_section, self._defaults
        all_sections = itertools.chain((defaults,), self._sections.items())
        for section, options in all_sections:
            for name, val in options.items():
                if isinstance(val, list):
                    val = '\n'.join(val).rstrip()
                options[name] = self._interpolation.before_read(
                    self, section, name, val)


def _getNode(node, path):
    if len(path) == 0:
        return node
    key = path[0].strip()
    return _getNode(node.getNode(key), path[1:])


# end of file
