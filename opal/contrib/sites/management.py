"""
Creates the default Site object.
"""

from opal.dispatch import dispatcher
from opal.db.models import signals
from opal.contrib.sites.models import Site
from opal.contrib.sites import models as site_app

def create_default_site(app, created_models, verbosity):
    if Site in created_models:
        if verbosity >= 2:
            print "Creating example.com Site object"
        s = Site(domain="example.com", name="example.com")
        s.save()

dispatcher.connect(create_default_site, sender=site_app, signal=signals.post_syncdb)
