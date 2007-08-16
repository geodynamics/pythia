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


from View import View
from opal.http import Http404


class ListView(View):
    """
    Generic list of objects.

    Templates: ``<app_label>/<model_name>_list.html``
    Context:
        object_list
            list of objects
        is_paginated
            are the results paginated?
        results_per_page
            number of objects per page (if paginated)
        has_next
            is there a next page?
        has_previous
            is there a prev page?
        page
            the current page
        next
            the next page
        previous
            the previous page
        pages
            number of pages, total
        hits
            number of objects, total
    """


    defaultTemplateNameTag = "list"


    def __init__(self, queryset, allow_empty=True, **kwds):
        View.__init__(self, queryset.model, **kwds)
        self.queryset = queryset
        self.allow_empty = allow_empty
        return


    def contextDictionary(self, request):
        if not self.allow_empty and len(self.queryset) == 0:
            raise Http404()
        dct = super(ListView, self).contextDictionary(request)
        dct.update({
            '%s_list' % self.template_object_name: self.queryset,
            'is_paginated': False
        })
        return dct


# end of file
