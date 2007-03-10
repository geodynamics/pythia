#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                      California Institute of Technology
#                        (C) 2007  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


class Query(object):

    def apply(self, queryset):
        raise NotImplementedError()

    def get(self, queryset):
        queryset = self.apply(queryset)
        return queryset.get()


class ObjectIdQuery(Query):

    def __init__(self, object_id):
        Query.__init__(self)
        self.object_id = object_id

    def apply(self, queryset):
        return queryset.filter(pk=self.object_id)

    def __str__(self):
        return "object_id=%s" % self.object_id


class ObjectSlugQuery(Query):

    def __init__(self, slug, slug_field):
        Query.__init__(self)
        self.slug = slug
        self.slug_field = slug_field

    def apply(self, queryset):
        return queryset.filter(**{self.slug_field: self.slug})

    def __str__(self):
        return "%s='%s'" % (self.slug_field, self.slug)


def objectQuery(object_id=None, slug=None, slug_field=None):
    if object_id:
        query = ObjectIdQuery(object_id)
    elif slug and slug_field:
        query = ObjectSlugQuery(slug, slug_field)
    else:
        raise AttributeError, "Object query must be created with either an object_id or a slug/slug_field."
    return query


# end of file
