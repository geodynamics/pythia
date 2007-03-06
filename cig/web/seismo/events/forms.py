#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                       cig.web.seismo.events
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
from models import Event, DataSource, Region, Source


class AddSingleSourceEventManipulator(Source.AddManipulator):

    def __init__(self):
        super(AddSingleSourceEventManipulator, self).__init__()
        # replace generic fields with custom fields

        del self['event']
        del self['dataSource']
        del self['region']
        self.fields.extend([forms.TextField('name',        maxlength=100,  is_required=True),
                            forms.TextField('dataSource',  maxlength=100,  is_required=True),
                            forms.TextField('region',      maxlength=100,  is_required=True),
                            ])
        return

    def save(self, new_data, user):
        from datetime import datetime
        
        # Create the new Event.
        event = Event.objects.create(user = user,
                                     name = new_data['name'])

        # Create the DataSource and Region.
        dataSource, created = DataSource.objects.get_or_create(name = new_data['dataSource'])
        region, created = Region.objects.get_or_create(name = new_data['region'])
        
        # Add the Source.
        args = {}
        for k,v in new_data.items():
            args[k] = v
        args['event'] = event
        args['dataSource'] = dataSource
        args['region'] = region
        args['when'] = datetime.combine(args['when_date'], args['when_time'])
        del args['name']
        del args['when_date']
        del args['when_time']
        source = Source.objects.create(**args)

        return event


class UploadEventManipulator(forms.Manipulator):
    
    def __init__(self):
        super(UploadEventManipulator, self).__init__()
        self.fields = [
            forms.TextField('name', maxlength=100, is_required=True),
            forms.FileUploadField(field_name='cmtsolution', is_required=True),
            ]

    def get_validation_errors(self, new_data):
        from cig.seismo.events import CMTSolution
        
        errors = super(UploadEventManipulator, self).get_validation_errors(new_data)
        
        if not errors.get('cmtsolution'):
            try:
                cmtSolution = new_data['cmtsolution']['content']
                CMTSolution.parse(cmtSolution)
            except CMTSolution.ParseError:
                errors['cmtsolution'] = ['Please select a file in CMTSOLUTION format.']

        return errors

    def save(self, new_data, user):
        from cig.seismo.events import CMTSolution

        # Parse the uploaded CMTSOLUTION file.
        cmtSolution = new_data['cmtsolution']['content']
        cmtSolutionList = CMTSolution.parse(cmtSolution)

        # Create the new event.
        event = Event.objects.create(user = user,
                                     name = new_data['name'])

        # Add each source.
        for cmtSolution in cmtSolutionList:
            Source.saveSource(event, cmtSolution)

        return event


# end of file
