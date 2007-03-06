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


from django.conf.urls.defaults import *
from models import Event, Source


event_list_detail_args = {
    'queryset': Event.user_objects.all(),
    'allow_empty': True,
}

event_detail_args = {
    'queryset': Event.user_objects.all(),
}

event_create_update_args = {
    'model': Event,
    'post_save_redirect': '/specfem3dglobe/events/',
    'follow': { 'user': False },
    }

event_delete_args = {
    'model': Event,
    'post_delete_redirect': '/specfem3dglobe/events/',
    }

source_detail_args = {
    'queryset': Source.objects.all(),
}

source_create_update_args = {
    'model': Source,
    'post_save_redirect': '/specfem3dglobe/events/',
    }

source_delete_args = {
    'model': Source,
    'post_delete_redirect': '/specfem3dglobe/events/',
    }


urlpatterns = patterns('',
    (r'^$', 'django.views.generic.list_detail.object_list', event_list_detail_args),
    (r'^search/$', 'cig.web.seismo.events.views.search'),
    (r'^add/$', 'cig.web.seismo.events.views.add'),
    (r'^upload/$', 'cig.web.seismo.events.views.upload'),
    (r'^sources/(?P<object_id>\d+)/$', 'django.views.generic.list_detail.object_detail', source_detail_args),
    (r'^sources/(?P<object_id>\d+)/edit/$', 'django.views.generic.create_update.update_object', source_create_update_args),
    (r'^sources/(?P<object_id>\d+)/delete/$', 'django.views.generic.create_update.delete_object', source_delete_args),
    (r'^(?P<object_id>\d+)/$', 'django.views.generic.list_detail.object_detail', event_detail_args),
    (r'^(?P<object_id>\d+)/edit/$', 'django.views.generic.create_update.update_object', event_create_update_args),
    (r'^(?P<object_id>\d+)/delete/$', 'django.views.generic.create_update.delete_object', event_delete_args),
)


# end of file
