from opal.conf import settings
from opal.conf.urls.defaults import *

if settings.USE_I18N:
    i18n_view = 'opal.views.i18n.javascript_catalog'
else:
    i18n_view = 'opal.views.i18n.null_javascript_catalog'

urlpatterns = patterns('',
    ('^$', 'opal.contrib.admin.views.main.index'),
    ('^r/(\d+)/(.*)/$', 'opal.views.defaults.shortcut'),
    ('^jsi18n/$', i18n_view, {'packages': 'opal.conf'}),
    ('^logout/$', 'opal.contrib.auth.views.logout'),
    ('^password_change/$', 'opal.contrib.auth.views.password_change'),
    ('^password_change/done/$', 'opal.contrib.auth.views.password_change_done'),
    ('^template_validator/$', 'opal.contrib.admin.views.template.template_validator'),

    # Documentation
    ('^doc/$', 'opal.contrib.admin.views.doc.doc_index'),
    ('^doc/bookmarklets/$', 'opal.contrib.admin.views.doc.bookmarklets'),
    ('^doc/tags/$', 'opal.contrib.admin.views.doc.template_tag_index'),
    ('^doc/filters/$', 'opal.contrib.admin.views.doc.template_filter_index'),
    ('^doc/views/$', 'opal.contrib.admin.views.doc.view_index'),
    ('^doc/views/jump/$', 'opal.contrib.admin.views.doc.jump_to_view'),
    ('^doc/views/(?P<view>[^/]+)/$', 'opal.contrib.admin.views.doc.view_detail'),
    ('^doc/models/$', 'opal.contrib.admin.views.doc.model_index'),
    ('^doc/models/(?P<app_label>[^\.]+)\.(?P<model_name>[^/]+)/$', 'opal.contrib.admin.views.doc.model_detail'),
#    ('^doc/templates/$', 'opal.views.admin.doc.template_index'),
    ('^doc/templates/(?P<template>.*)/$', 'opal.contrib.admin.views.doc.template_detail'),

    # Add/change/delete/history
    ('^([^/]+)/([^/]+)/$', 'opal.contrib.admin.views.main.change_list'),
    ('^([^/]+)/([^/]+)/add/$', 'opal.contrib.admin.views.main.add_stage'),
    ('^([^/]+)/([^/]+)/(.+)/history/$', 'opal.contrib.admin.views.main.history'),
    ('^([^/]+)/([^/]+)/(.+)/delete/$', 'opal.contrib.admin.views.main.delete_stage'),
    ('^([^/]+)/([^/]+)/(.+)/$', 'opal.contrib.admin.views.main.change_stage'),
)

del i18n_view
