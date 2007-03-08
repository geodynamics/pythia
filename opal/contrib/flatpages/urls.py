from opal.conf.urls.defaults import *

urlpatterns = patterns('opal.contrib.flatpages.views',
    (r'^(?P<url>.*)$', 'flatpage'),
)
