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


from models import Station, StationList, StationNetwork
import support

from opal import forms
from opal.components import WebComponent
from opal.db.queries import primaryInquirer
from opal.http import HttpResponseRedirect
from opal.shortcuts import get_object_or_404, render_to_response
from opal.template.context import RequestContext


class StationBrowser(WebComponent):


    name = "stations"


    models = [Station, StationList, StationNetwork]


    def __init__(self, home="/"):
        WebComponent.__init__(self)

        self.home = home # '/specfem3dglobe/stations/'
        
        from opal.contrib.auth.decorators import login_required
        self.urlpatterns = self.patterns(
            (r'^$', login_required(self.index)),
            (r'^create/$', login_required(self.createStationList)),
            (r'^upload/$', login_required(self.uploadStationList)),
            (r'^(?P<object_id>\d+)/$', self.stationListDetail),
            (r'^(?P<object_id>\d+)/edit/$', self.editStationList),
            (r'^(?P<object_id>\d+)/delete/$', self.deleteStationList),
            (r'^(?P<object_id>\d+)/gearth\.kml$', self.stationListDetailGEarth),
            )

        return


    def index(self, request):
        station_lists = StationList.objects.filter(user__exact=request.user)
        return render_to_response('stations/index.html',
                                  {'station_lists': station_lists },
                                  RequestContext(request, {}))


    def createStationList(self, request):
        from os.path import dirname
        from pkg_resources import resource_stream

        actionChoices = (
            (0, 'Create an empty list of stations.'),
            (1, 'Create a default list of stations.'),
            )
        class Manipulator(forms.Manipulator):
            def __init__(self):
                super(Manipulator, self).__init__()
                self.fields = [
                    forms.TextField('name', maxlength=100, is_required=True),
                    forms.RadioSelectField('action', choices=actionChoices, is_required=True)
                    ]

        manipulator = Manipulator()

        if request.method == 'POST':
            new_data = request.POST.copy()
            errors = manipulator.get_validation_errors(new_data)
            if not errors:
                manipulator.do_html2python(new_data)
                stationList = StationList.objects.create(user = request.user,
                                                         name = new_data['name'])
                if new_data['action'] == "1":
                    stream = resource_stream(__name__, "STATIONS")
                    support.parse_station_list(stationList, stream)
                #url = "%s/%i/" % (dirname(dirname(request.path)), stationList.id)
                url = self.home
                return HttpResponseRedirect(url)
        else:
            errors = {}
            new_data = {'action': 1}

        form = forms.FormWrapper(manipulator, new_data, errors)
        return render_to_response('stations/stationlist_create.html',
                                  {'form': form},
                                  RequestContext(request, {}))


    def uploadStationList(self, request):
        from os.path import dirname

        manipulator = support.UploadStationListManipulator()

        if request.method == 'POST':
            new_data = request.POST.copy()
            new_data.update(request.FILES)
            errors = manipulator.get_validation_errors(new_data)
            if not errors:
                manipulator.do_html2python(new_data)
                stationList = manipulator.save(new_data, request.user)
                #url = "%s/%i/" % (dirname(dirname(request.path)), stationList.id)
                url = self.home
                return HttpResponseRedirect(url)
        else:
            errors = new_data = {}

        form = forms.FormWrapper(manipulator, new_data, errors)
        return render_to_response('stations/stationlist_upload.html',
                                  {'form': form},
                                  RequestContext(request, {}))


    def stationListDetail(self, request, object_id):
        return self.genericObjectDetail(
            request,
            queryset = StationList.objects.all(),
            query = primaryInquirer.newQuery(object_id),
            )


    def editStationList(self, request, object_id):
        return self.genericUpdateObject(
            request,
            model = StationList,
            query = primaryInquirer.newQuery(object_id),
            post_save_redirect = self.home,
            follow = { 'user': False },
            )


    def deleteStationList(self, request, object_id):
        return self.genericDeleteObject(
            request,
            model = StationList,
            query = primaryInquirer.newQuery(object_id),
            post_delete_redirect = self.home,
            )


    def stationListDetailGEarth(self, request, object_id):
        stationList = get_object_or_404(StationList, id=object_id)
        return support.station_list_gearth(
            request,
            queryset = stationList.station_set.all(),
            extra_context = {'name': stationList.name}
            )


# end of file
