#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                       cig.web.seismo.events
#
# Copyright (c) 2007, California Institute of Technology
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


from models import Event, Source, DataSource, Region
from parsers import HarvardCMTSearchResultsParser

from cig.seismo.events import CMTSolution
from opal import forms
from opal.http import HttpResponseRedirect
from opal.shortcuts import render_to_response
from opal.template.context import RequestContext


class EventBrowser(WebComponent):


    models = [Event, Source, DataSource, Region]


    def __init__(self, home):

        self.home = home # '/specfem3dglobe/events/'
        
        self.urlpatterns = self.patterns(
            (r'^$', self.eventList),
            (r'^search/$', self.eventSearch),
            (r'^add/$', self.addEvent),
            (r'^upload/$', self.uploadEvent),
            (r'^sources/(?P<object_id>\d+)/$', self.sourceDetail),
            (r'^sources/(?P<object_id>\d+)/edit/$', self.editSource),
            (r'^sources/(?P<object_id>\d+)/delete/$', self.deleteSource),
            (r'^(?P<object_id>\d+)/$', self.eventDetail),
            (r'^(?P<object_id>\d+)/edit/$', self.editEvent),
            (r'^(?P<object_id>\d+)/delete/$', self.deleteEvent),
            )
        
        return


    # views

    def eventList(self, request):
        return self.genericObjectList(
            request,
            queryset = Event.user_objects.all(),
            allow_empty = True,
            )


    def eventDetail(self, request):
        return self.genericObjectDetail(
            request,
            queryset = Event.user_objects.all()
            )


    def editEvent(self, request):
        return self.genericUpdateObject(
            request,
            model = Event,
            post_save_redirect = self.home,
            follow: { 'user': False },
            )


    def deleteEvent(self, request):
        return self.genericDeleteObject(
            request,
            model: Event,
            post_delete_redirect: self.home,
            )


    def eventSearch(self, request):
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


    def addEvent(self, request):
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


    def uploadEvent(self, request):
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


    # views -- sources

    def sourceDetail(self, request):
        return self.genericObjectDetail(
            request,
            queryset = Source.objects.all()
            )


    def editSource(self, request):
        return self.genericUpdateObject(
            request,
            model = Source,
            post_save_redirect = self.home,
            follow: { 'user': False },
            )


    def deleteSource(self, request):
        return self.genericDeleteObject(
            request,
            model: Source,
            post_delete_redirect: self.home,
            )


# end of file
