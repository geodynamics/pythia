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


from django.db import models
from django.contrib.auth.models import User
from cig.web.managers import CurrentUserManager


class Region(models.Model):
    name = models.CharField(maxlength=100, primary_key=True)
    def __str__(self): return self.name


class DataSource(models.Model):
    name = models.CharField(maxlength=100, primary_key=True)
    def __str__(self): return self.name


class Event(models.Model):

    # each user has a list of their own events
    user = models.ForeignKey(User)
    
    name = models.CharField(maxlength=100)

    # managers
    objects = models.Manager()
    user_objects = CurrentUserManager()

    def __str__(self): return self.name

    def delete(self):
        self.source_set.all().delete()
        super(Event, self).delete()


class Source(models.Model):

    # an event is composed of one or more sources
    event = models.ForeignKey(Event)

    dataSource = models.ForeignKey(DataSource)

    when = models.DateTimeField()
    microsecond = models.IntegerField()
    
    sourceLatitude = models.FloatField(max_digits=19, decimal_places=10)
    sourceLongitude = models.FloatField(max_digits=19, decimal_places=10)
    sourceDepth = models.FloatField(max_digits=19, decimal_places=10)
    sourceMB = models.FloatField(max_digits=19, decimal_places=10)
    sourceMs = models.FloatField(max_digits=19, decimal_places=10)
    region = models.ForeignKey(Region)
    
    eventName = models.CharField(maxlength=100)
    timeShift = models.FloatField(max_digits=19, decimal_places=10)
    halfDuration = models.FloatField(max_digits=19, decimal_places=10)
    latitude = models.FloatField(max_digits=19, decimal_places=10)
    longitude = models.FloatField(max_digits=19, decimal_places=10)
    depth = models.FloatField(max_digits=19, decimal_places=10)
    Mrr = models.FloatField(max_digits=19, decimal_places=10)
    Mtt = models.FloatField(max_digits=19, decimal_places=10)
    Mpp = models.FloatField(max_digits=19, decimal_places=10)
    Mrt = models.FloatField(max_digits=19, decimal_places=10)
    Mrp = models.FloatField(max_digits=19, decimal_places=10)
    Mtp = models.FloatField(max_digits=19, decimal_places=10)

    def __str__(self): return self.eventName

    def _getMrrStr2f(self): return "%.2f" % (self.Mrr * 1.0e-26)
    def _getMttStr2f(self): return "%.2f" % (self.Mtt * 1.0e-26)
    def _getMppStr2f(self): return "%.2f" % (self.Mpp * 1.0e-26)
    def _getMrtStr2f(self): return "%.2f" % (self.Mrt * 1.0e-26)
    def _getMrpStr2f(self): return "%.2f" % (self.Mrp * 1.0e-26)
    def _getMtpStr2f(self): return "%.2f" % (self.Mtp * 1.0e-26)

    mrr = property(_getMrrStr2f)
    mtt = property(_getMttStr2f)
    mpp = property(_getMppStr2f)
    mrt = property(_getMrtStr2f)
    mrp = property(_getMrpStr2f)
    mtp = property(_getMtpStr2f)

    def saveSource(cls, event, cmtSolution):
        import datetime

        when = datetime.datetime(cmtSolution.year,
                                 cmtSolution.month,
                                 cmtSolution.day,
                                 cmtSolution.hour,
                                 cmtSolution.minute,
                                 cmtSolution.second)
        
        dataSource, created = DataSource.objects.get_or_create(name = cmtSolution.dataSource)
        region, created = Region.objects.get_or_create(name = cmtSolution.regionName)
        
        source = Source(
            event             = event,
            dataSource        = dataSource,
            when              = when,
            microsecond       = cmtSolution.microsecond,
            sourceLatitude    = cmtSolution.sourceLatitude,
            sourceLongitude   = cmtSolution.sourceLongitude,
            sourceDepth       = cmtSolution.sourceDepth,
            sourceMB          = cmtSolution.sourceMB,
            sourceMs          = cmtSolution.sourceMs,
            region            = region,
            eventName         = cmtSolution.eventName,
            timeShift         = cmtSolution.timeShift,
            halfDuration      = cmtSolution.halfDuration,
            latitude          = cmtSolution.latitude,
            longitude         = cmtSolution.longitude,
            depth             = cmtSolution.depth,
            Mrr               = cmtSolution.Mrr,
            Mtt               = cmtSolution.Mtt,
            Mpp               = cmtSolution.Mpp,
            Mrt               = cmtSolution.Mrt,
            Mrp               = cmtSolution.Mrp,
            Mtp               = cmtSolution.Mtp,
            )
        
        source.save()
        return
    
    saveSource = classmethod(saveSource)


# end of file
