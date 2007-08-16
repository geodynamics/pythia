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


from opal.http import HttpResponse
from opal.template import RequestContext


class View(object):


    def __init__(self, model=None, controller=None, subviews=None,
                 template_name=None, template_loader=None,
                 extra_context=None, context_processors=None,
                 template_object_name='object',
                 mimetype=None):
        self.model = model
        if controller is None:
            from opal.controllers import NoController
            self.controller = NoController()
        else:
            self.controller = controller
        self.controller.view = self
        self.subviews = subviews
        if template_name:
            self.template_name = template_name
        else:
            self.template_name = "%s/%s_%s.html" % (self.model._meta.app_label,
                                                    self.model._meta.object_name.lower(),
                                                    self.templateNameTag)
        if template_loader is None:
            from opal.template import loader
            self.template_loader = loader
        else:
            self.template_loader = template_loader
        if extra_context is None:
            self.extra_context = {}
        else:
            self.extra_context = extra_context
        self.context_processors = context_processors
        self.template_object_name = template_object_name
        self.mimetype = mimetype
        return


    def response(self, request):
        return HttpResponse(self.render(request), mimetype=self.mimetype)


    def render(self, request):
        c = self.requestContext(request)
        c = self.addExtraContext(c)
        t = self.loadTemplate()
        return t.render(c)


    def _getTemplateNameTag(self):
        return self.controller.templateNameTag
    templateNameTag = property(_getTemplateNameTag)


    def loadTemplate(self):
        return self.template_loader.get_template(self.template_name)


    def addExtraContext(self, c):
        for key, value in self.extra_context.items():
            if callable(value):
                c[key] = value()
            else:
                c[key] = value
        return c


    def requestContext(self, request):
        return RequestContext(
            request,
            self.contextDictionary(request),
            self.context_processors,
            )


    def contextDictionary(self, request):
        dct = self.controller.contextDictionary(request)
        if self.subviews is not None:
            subviews = {}
            for name, view in self.subviews.iteritems():
                subviews[name] = view.render(request)
            dct['subviews'] = subviews
        return dct


# end of file
