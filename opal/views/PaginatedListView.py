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


from ListView import ListView
from opal.core.paginator import ObjectPaginator, InvalidPage
from opal.http import Http404


class PaginatedListView(ListView):
    """
    Paginated list of objects.

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


    def __init__(self, queryset, paginate_by, page=None, **kwds):
        ListView.__init__(self, queryset, **kwds)
        self.paginate_by = paginate_by
        self.page = page
        return


    def contextDictionary(self, request):
        queryset = self.queryset._clone()
        paginator = ObjectPaginator(queryset, self.paginate_by)
        page = self.page
        if not page:
            page = request.GET.get('page', 1)
        try:
            page = int(page)
            object_list = paginator.get_page(page - 1)
        except (InvalidPage, ValueError):
            if page == 1 and self.allow_empty:
                object_list = []
            else:
                raise Http404()
        dct = super(ListView, self).contextDictionary(request)
        dct.update({
            '%s_list' % self.template_object_name: object_list,
            'is_paginated': paginator.pages > 1,
            'results_per_page': self.paginate_by,
            'has_next': paginator.has_next_page(page - 1),
            'has_previous': paginator.has_previous_page(page - 1),
            'page': page,
            'next': page + 1,
            'previous': page - 1,
            'pages': paginator.pages,
            'hits' : paginator.hits,
        })
        return dct


# end of file
