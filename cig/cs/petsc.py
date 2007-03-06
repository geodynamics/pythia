#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               cig.cs
#
# Copyright (c) 2006, California Institute of Technology
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#
#    * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#
#    * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#
#    * Neither the name of the California Institute of Technology nor
#    the names of its contributors may be used to endorse or promote
#    products derived from this software without specific prior
#    written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from pyre.applications.CommandlineParser import CommandlineParser


class PetscCommandlineParser(CommandlineParser):
    """A parser which mimics PETSc's command line processing."""

    # The logic used here is derived from the 'while' loop at the end
    # of PetscOptionsInsert().  However, this doesn't check for "bad"
    # MPICH options, as these should have been removed by MPI_Init().


    def _parse(self, argv, root):
        
        self.action = None
        self.argv = argv
        self.processed = []
        self.unprocessed = []
        
        while self.argv:
            
            arg = self.argv.pop(0)
            
            iname = self._filterNonOptionArgument(arg)
            if iname is None:
                continue
            
            if iname.lower() == "options_file":
                # NYI
                if self.argv:
                    filename = self.argv.pop(0)
                else:
                    pass # error
                continue

            if (not self.argv) or self._isOptionArgument(self.argv[0]):
                iname, value = self._parseArgument(iname)
            else:
                value = self.argv.pop(0)

            self._processArgument(iname, value, root)

        return


    def _optionPrefix(self, arg):
        for prefix in self.prefixes:
            if arg.startswith(prefix):
                return prefix
        return None


    def _isOptionArgument(self, arg):
        import string
        prefix = self._optionPrefix(arg)
        if prefix is not None:
            candidate = arg[len(prefix):]
            if (prefix == "-" and
                len(candidate) > 0 and
                candidate[0] in string.digits):
                return False
            return True
        return False


    def _filterNonOptionArgument(self, arg):
        
        prefix = self._optionPrefix(arg)
        
        if prefix is not None:
            self._debug.line("    prefix: '%s starts with '%s'" % (arg, prefix))
            candidate = arg[len(prefix):]
            return candidate
        
        # prefix matching failed; leave this argument alone
        self._debug.line("    prefix: '%s' is not an option" % arg)
        self.processed.append(arg)
        return None



from pyre.components import Component


class Petsc(Component):


    def updateConfiguration(self, registry):
        self.options = [
            (name, descriptor.value) for name, descriptor in registry.properties.iteritems()
            ]
        return []


    def getArgs(self):
        args = []
        for iname, value in self.options:
            args.append('-' + iname)
            if value != 'true':
                args.append(value)
        return args


    def __init__(self, name):
        Component.__init__(self, name, name)
        self.options = []
        return



from pyre.inventory.Facility import Facility


class PetscFacility(Facility):


    def __init__(self, name):
        Facility.__init__(self, name=name, factory=Petsc, args=[name])
        return


    def _retrieveComponent(self, instance, componentName):
        petsc = Petsc(componentName)

        import pyre.parsing.locators
        locator = pyre.parsing.locators.simple('built-in')

        return petsc, locator



# end of file 
