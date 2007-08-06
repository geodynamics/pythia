#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                      cig.web.seismo.stations
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


from opal.conf.urls.defaults import *
from models import Station, StationList, StationNetwork


stationlist_delete_args = {
    'model': StationList,
    'post_delete_redirect': '/specfem3dglobe/stations/',
    }


stationlist_create_update_args = {
    'model': StationList,
    'post_save_redirect': '/specfem3dglobe/stations/',
    'follow': { 'user': False },
    }


urlpatterns = patterns('',
    (r'^$', 'cig.web.seismo.stations.views.index'),
    (r'^create/$', 'cig.web.seismo.stations.views.create'),
    (r'^default/$', 'cig.web.seismo.stations.views.default'),
    (r'^upload/$', 'cig.web.seismo.stations.views.upload'),
    (r'^(?P<object_id>\d+)/$', 'opal.views.generic.list_detail.object_detail', {'queryset': StationList.objects.all()}),
    (r'^(?P<object_id>\d+)/edit/$', 'opal.views.generic.create_update.update_object', stationlist_create_update_args),
    (r'^(?P<object_id>\d+)/delete/$', 'opal.views.generic.create_update.delete_object', stationlist_delete_args),
    (r'^(?P<object_id>\d+)/gearth\.kml$','cig.web.seismo.stations.views.stationlist_detail_gearth'),
)


# end of file
