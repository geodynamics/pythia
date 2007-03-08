from opal.conf import settings
from opal.core.exceptions import ObjectDoesNotExist, ImproperlyConfigured
from opal.core import validators
from opal.db import backend, connection
from opal.db.models.loading import get_apps, get_app, get_models, get_model, register_models
from opal.db.models.query import Q
from opal.db.models.manager import Manager
from opal.db.models.base import Model, AdminOptions
from opal.db.models.fields import *
from opal.db.models.fields.related import ForeignKey, OneToOneField, ManyToManyField, ManyToOneRel, ManyToManyRel, OneToOneRel, TABULAR, STACKED
from opal.db.models.fields.generic import GenericRelation, GenericRel, GenericForeignKey
from opal.db.models import signals
from opal.utils.functional import curry
from opal.utils.text import capfirst

# Admin stages.
ADD, CHANGE, BOTH = 1, 2, 3

# Decorator. Takes a function that returns a tuple in this format:
#     (viewname, viewargs, viewkwargs)
# Returns a function that calls urlresolvers.reverse() on that data, to return
# the URL for those parameters.
def permalink(func):
    from opal.core.urlresolvers import reverse
    def inner(*args, **kwargs):
        bits = func(*args, **kwargs)
        viewname = bits[0]
        return reverse(bits[0], None, *bits[1:2])
    return inner

class LazyDate(object):
    """
    Use in limit_choices_to to compare the field to dates calculated at run time
    instead of when the model is loaded.  For example::

        ... limit_choices_to = {'date__gt' : models.LazyDate(days=-3)} ...

    which will limit the choices to dates greater than three days ago.
    """
    def __init__(self, **kwargs):
        self.delta = datetime.timedelta(**kwargs)

    def __str__(self):
        return str(self.__get_value__())

    def __repr__(self):
        return "<LazyDate: %s>" % self.delta

    def __get_value__(self):
        return datetime.datetime.now() + self.delta

    def __getattr__(self, attr):
        return getattr(self.__get_value__(), attr)
