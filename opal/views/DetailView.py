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
from opal.template import RequestContext
from opal.http import Http404, HttpResponse
from opal.core.xheaders import populate_xheaders


class DetailView(View):
    """
    Generic view of an object.

    Templates: ``<app_label>/<model_name>_detail.html``
    Context:
        object
            the object
    """


    templateNameTag = "detail"


    def __init__(self, queryset, query,
                 template_name_field=None, **kwds):
        View.__init__(self, queryset=queryset, **kwds)
        self.query = query
        self.template_name_field = template_name_field
        return


    def response(self, request):
        model = self.queryset.model
        try:
            obj = self.query.get(self.queryset)
        except ObjectDoesNotExist:
            raise Http404, "No %s found matching the query '%s'" % (model._meta.verbose_name, query)
        t = self.loadTemplate(obj)
        c = RequestContext(request, {template_object_name: obj}, self.context_processors)
        c = self.addExtraContext(c)
        response = HttpResponse(t.render(c), mimetype=self.mimetype)
        populate_xheaders(request, response, model, getattr(obj, obj._meta.pk.name))
        return response


    def loadTemplate(self, obj):
        if self.template_name_field:
            template_name_list = [getattr(obj, self.template_name_field), self.template_name]
            t = self.template_loader.select_template(template_name_list)
        else:
            t = super(DetailView, self).loadTemplate()
        return t


# end of file
