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


from opal.db import models
from opal.contrib.auth.models import User
from cig.web.managers import CurrentUserManager


STATION_STATUS_TYPES = (
    (0, 'closed'),
    (1, 'open'),
)


class StationNetwork(models.Model):
    code = models.CharField(maxlength=10, primary_key=True) # 3-5 chars currently
    name = models.CharField(maxlength=100)

    def __str__(self): return self.code


class StationList(models.Model):

    # each user has their own station lists
    user = models.ForeignKey(User)

    name = models.CharField(maxlength=100)

    # managers
    objects = models.Manager()
    user_objects = CurrentUserManager()

    def __str__(self): return self.name

    def delete(self):
        self.station_set.all().delete()
        super(StationList, self).delete()


class Station(models.Model):
    
    # each user has their own stations
    stationList = models.ForeignKey(StationList)

    code = models.CharField(maxlength=10) # 3-4 chars currently
    name = models.CharField(maxlength=100)
    network = models.ForeignKey(StationNetwork, null=True)
    status = models.IntegerField(choices=STATION_STATUS_TYPES, default=1)
    latitude = models.FloatField(max_digits=19, decimal_places=10)
    longitude = models.FloatField(max_digits=19, decimal_places=10)
    elevation = models.FloatField(max_digits=19, decimal_places=10)
    bur = models.FloatField(max_digits=19, decimal_places=10, default=0.0)

    def __str__(self): return self.code


# end of file
