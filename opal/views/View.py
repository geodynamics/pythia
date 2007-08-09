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


class View(object):


    def __init__(self, model, controller=None,
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
        __pychecker__ = 'unusednames=request'
        raise NotImplementedError("class %r must override 'response'" % self.__class__.__name__)


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


    def globalContext(self):
        return self.controller.globalContext()


# end of file
