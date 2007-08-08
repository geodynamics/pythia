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


from opal import forms
from models import Station, StationList, StationNetwork


# support code


def parse_station_list(stationList, stream):

    # discard the count
    stream.readline()
    
    for line in stream:

        # parse the line
        code, network, latitude, longitude, elevation, bur = line.split()
        latitude, longitude = float(latitude), float(longitude)
        elevation, bur = float(elevation), float(bur)

        if stationList is None:
            continue

        # get/create the network entry
        network, created = StationNetwork.objects.get_or_create(code = network, defaults = { 'name': "" })

        # create the station
        station = Station.objects.create(stationList = stationList,
                                         code = code,
                                         name = "",
                                         network = network,
                                         status = 1,
                                         latitude = latitude,
                                         longitude = longitude,
                                         elevation = elevation,
                                         bur = bur)
    return


class UploadStationListManipulator(forms.Manipulator):
    
    def __init__(self):
        super(UploadStationListManipulator, self).__init__()
        self.fields = [
            forms.TextField('name', maxlength=100, is_required=True),
            forms.FileUploadField(field_name='stations', is_required=True),
            ]

    def get_validation_errors(self, new_data):
        from StringIO import StringIO
        
        errors = super(UploadStationListManipulator, self).get_validation_errors(new_data)
        
        if not errors.get('stations'):
            try:
                stations = new_data['stations']['content']
                stream = StringIO(stations)
                parse_station_list(None, stream)
            except Exception:
                errors['stations'] = ['Please select a file in STATIONS format.']

        return errors

    def save(self, new_data, user):
        from StringIO import StringIO

        # Create the new station list.
        stationList = StationList.objects.create(user = user,
                                                 name = new_data['name'])
        
        # Parse the uploaded STATIONS file.
        stations = new_data['stations']['content']
        stream = StringIO(stations)
        parse_station_list(stationList, stream)

        return stationList


# move to shared location
def gearth_object_list(request, **kwds):
    from opal.views.generic.list_detail import object_list
    return object_list(request,
                       mimetype='application/vnd.google-earth',
                       **kwds)


def station_list_gearth(request, **kwds):
    return gearth_object_list(request,
                              template_name='stations/station_list_gearth.kml',
                              **kwds)


# end of file
