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
from opal.core.exceptions import ObjectDoesNotExist
from opal.http import Http404, HttpResponse
from opal.template import RequestContext


class DetailView(View):
    """
    Generic view of an object.

    Templates: ``<app_label>/<model_name>_detail.html``
    Context:
        object
            the object
    """


    defaultTemplateNameTag = "detail"


    def __init__(self, model, query, template_name_field=None, **kwds):
        View.__init__(self, model, **kwds)
        self.query = query
        self.obj = None
        self.template_name_field = template_name_field
        return


    def response(self, request):
        self.obj = self.getObject()
        # Give the controller a chance to respond to this request.
        return self.controller.response(request)


    def render(self, request):
        t = self.loadTemplate()
        c = self.createContext(request)
        response = HttpResponse(t.render(c), mimetype=self.mimetype)
        self.controller.decorateResponse(response, request)
        return response


    def getObject(self):
        try:
            obj = self.query.get(self.model._default_manager.all())
        except ObjectDoesNotExist:
            raise Http404("No %s found matching the query '%s'" % (self.model._meta.verbose_name, self.query))
        return obj


    def loadTemplate(self):
        if self.template_name_field:
            template_name_list = [getattr(self.obj, self.template_name_field), self.template_name]
            t = self.template_loader.select_template(template_name_list)
        else:
            t = super(DetailView, self).loadTemplate()
        return t


    def createContext(self, request):
        c = RequestContext(request, self.globalContext(), self.context_processors)
        c = self.addExtraContext(c)
        return c


    def globalContext(self):
        context = super(DetailView, self).globalContext()
        context[self.template_object_name] = self.obj
        return context


# end of file
