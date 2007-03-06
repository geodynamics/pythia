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


# This is simple script to create initial SQL data for the database.
# The resulting SQL files are read automatically by Django when
# 'syncdb' is run.


# ~~~ input files ~~~

# Data from USGS <http://neic.usgs.gov/neis/station_book/>

# * station_comma_list.asc: "Station List - Spreadsheet Format"
# <http://neic.usgs.gov/neis/gis/station_comma_list.asc>

# * stationnetwork.txt -- Copy & pasted from the "Networks" page
# <http://neic.usgs.gov/neis/station_book/NETWORK.html>


txt = open("stationnetwork.txt", "r")
sql = open("stationnetwork.sql", "w")
for line in txt:
    code, name = line.split("\t")
    code = code.strip()
    if not code:
        continue
    name = name.strip().replace("'", "''")
    # Strip weird characters -- otherwise Django dies while rendering:
    #   "Could not decode to UTF-8 column 'name' with text 'Universit\ufffd di Calabria, Cosenza, Italy'"
    # There is no time to figure this out now.
    name = unicode(name, "utf-8", 'ignore')
    name = name.encode("utf-8")
    print >> sql, "INSERT INTO stations_stationnetwork (code, name) VALUES ('%s', '%s');" % (code, name)
txt.close()
sql.close()


txt = open("station_comma_list.asc", "r")
sql = open("station.sql", "w")
for line in txt:
    code, latitude, longitude, elevation, network, status, name = line.split(",")
    code = code.strip()
    if (not latitude) or (latitude == 'LATITUDE'):
        continue
    latitude = float(latitude)
    longitude = float(longitude)
    elevation = float(elevation)
    network = network.strip()
    if not network:
        network = 'NULL'
    else:
        network = "'%s'" % network
    if status == 'Open':
        status = 1
    else:
        status = 0
    name = name.strip().replace("'", "''")
    print >> sql, (
        "INSERT INTO stations_station (code, latitude, longitude, elevation, network_id, status, name, bur) "
        "VALUES ('%s', %f, %f, %f, %s, %d, '%s', 0.0);" %
        (code, latitude, longitude, elevation, network, status, name)
        )
txt.close()
sql.close()


# end of file
