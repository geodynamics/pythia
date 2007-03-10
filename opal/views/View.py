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


    def __init__(self, queryset,
                 template_name=None, template_loader=None,
                 extra_context=None, context_processors=None,
                 template_object_name='object',
                 mimetype=None):
        self.queryset = queryset
        if template_name:
            self.template_name = template_name
        else:
            model = queryset.model
            template_name = "%s/%s_%s.html" % (model._meta.app_label,
                                               model._meta.object_name.lower(),
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


    def response(self):
        raise NotImplementedError("class %r must override 'response'" % self.__class__.__name__)


    def loadTemplate(self):
        return self.template_loader.get_template(self.template_name)


    def addExtraContext(self, c):
        for key, value in self.extra_context.items():
            if callable(value):
                c[key] = value()
            else:
                c[key] = value
        return c


# end of file
