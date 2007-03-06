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


from cig.seismo.events import CMTSolution
from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from HTMLParser import HTMLParser
from models import DataSource, Region


def search(request):
    import urllib2

    if request.method == 'GET':
        return render_to_response('events/event_search.html',
                                  {},
                                  RequestContext(request, {})) 

    # Simply forward the search request to Harvard.
    query = request.POST.urlencode()
    url = "http://www.seismology.harvard.edu/cgi-bin/CMT3/form?" + query
    src = urllib2.urlopen(url)

    # Parse the results.
    parser = HarvardCMTSearchResultsParser()
    parser.feed(src.read())
    
    parser.close()
    src.close()

    # Make sure secondary objects exist in the database.
    for event in parser.cmtList:
        # The try-get()-except shouldn't be necessary, but simply
        # using save() causes Django to die in the database backend.
        try:
            ds = DataSource.objects.get(name=event.dataSource)
        except DataSource.DoesNotExist:
            ds = DataSource(event.dataSource)
            ds.save()
        try:
            ds = Region.objects.get(name=event.regionName)
        except:
            r = Region(event.regionName)
            r.save()
    
    return render_to_response('events/event_search_results.html',
                              {'event_list': parser.cmtList },
                              RequestContext(request, {})) 


def add(request):
    from forms import AddSingleSourceEventManipulator
    from os.path import dirname
    
    manipulator = AddSingleSourceEventManipulator()
    
    if request.method == 'POST':
        new_data = request.POST.copy()
        errors = manipulator.get_validation_errors(new_data)
        if not errors:
            manipulator.do_html2python(new_data)
            new_event = manipulator.save(new_data, request.user)
            url = "%s/%i/" % (dirname(dirname(request.path)), new_event.id)
            return HttpResponseRedirect(url)
    else:
        errors = new_data = {}

    form = forms.FormWrapper(manipulator, new_data, errors)
    return render_to_response('events/single_source_event_form.html',
                              {'form': form},
                              RequestContext(request, {}))


def upload(request):
    from forms import UploadEventManipulator
    from os.path import dirname
    
    manipulator = UploadEventManipulator()
    
    if request.method == 'POST':
        new_data = request.POST.copy()
        new_data.update(request.FILES)
        errors = manipulator.get_validation_errors(new_data)
        if not errors:
            manipulator.do_html2python(new_data)
            new_event = manipulator.save(new_data, request.user)
            url = "%s/%i/" % (dirname(dirname(request.path)), new_event.id)
            return HttpResponseRedirect(url)
    else:
        errors = new_data = {}

    form = forms.FormWrapper(manipulator, new_data, errors)
    return render_to_response('events/event_upload.html',
                              {'form': form},
                              RequestContext(request, {}))


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# support code


class HarvardCMTSearchResultsParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.state = 0
        self.cmtList = None
        
    def handle_starttag(self, tag, attrs):
        if self.state == 0:
            if tag == 'body':
                self.state = 1
        elif self.state == 2:
            if tag == 'pre':
                self.state = 3
        return

    def handle_endtag(self, tag):
        if tag == 'body':
            self.state = 0
        elif self.state == 3:
            if tag == 'pre':
                self.state = 1
        return

    def handle_data(self, data):
        if self.state == 1:
            if data.find('Output in CMTSOLUTION format') != -1:
                self.state = 2
        elif self.state == 3:
            self.cmtList = CMTSolution.parse(data)
        return


# end of file
