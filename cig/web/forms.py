#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                              cig.web
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


from django import forms


class TeeManipulator(forms.Manipulator):
    """Merges multiple Django Manipulators into one.  Useful when
    creating a custom form which creates/edits multiple Models on the
    same page.

    Django's inline editing is a bit limited (not to mention poorly
    documented) as of v0.95.

    """

    def __init__(self, manipulators):
        forms.Manipulator.__init__(self)
        self.manipulators = manipulators
        for key, manip in self.manipulators.iteritems():
            for field in manip.fields:
                field.field_name = key + field.field_name
            self.fields.extend(manip.fields)
        return

    def flatten_data(self):
        new_data = {}
        for key, manip in self.manipulators.iteritems():
            new_data.update(manip.flatten_data())
        return new_data

    def get_validation_errors(self, new_data):
        errors = {}
        for key, manip in self.manipulators.iteritems():
            errors.update(manip.get_validation_errors(new_data))
        return errors
    
    def do_html2python(self, new_data):
        for key, manip in self.manipulators.iteritems():
            manip.do_html2python(new_data)
        return

    def _revert_field_names(self, new_data):
        for key, manip in self.manipulators.iteritems():
            keyLen = len(key)
            for field in manip.fields:
                oldName = field.field_name[keyLen:]
                if new_data.has_key(field.field_name):
                    new_data.setlist(oldName, new_data.getlist(field.field_name))
                field.field_name = oldName
        return
    
    def save(self, new_data):
        self._revert_field_names(new_data)
        for key, manip in self.manipulators.iteritems():
            manip.save(new_data)
        return


# end of file
