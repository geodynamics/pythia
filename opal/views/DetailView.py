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
from opal.http import Http404


class DetailView(View):
    """
    Generic view of an object.

    Templates: ``<app_label>/<model_name>_detail.html``
    Context:
        object
            the object
    """


    defaultTemplateNameTag = "detail"


    def __init__(self, model, query=None, template_name_field=None, **kwds):
        View.__init__(self, model, **kwds)
        self.query = query
        self._obj = None
        self.template_name_field = template_name_field
        return


    def _getObj(self):
        if self._obj is None and self.query:
            try:
                self._obj = self.query.get(self.model._default_manager.all())
            except ObjectDoesNotExist:
                raise Http404("No %s found matching the query '%s'" % (self.model._meta.verbose_name, self.query))
        return self._obj
    obj = property(_getObj)


    def loadTemplate(self):
        if self.obj and self.template_name_field:
            template_name_list = [getattr(self.obj, self.template_name_field), self.template_name]
            t = self.template_loader.select_template(template_name_list)
        else:
            t = super(DetailView, self).loadTemplate()
        return t


    def contextDictionary(self, request):
        dct = super(DetailView, self).contextDictionary(request)
        if self.obj:
            dct[self.template_object_name] = self.obj
        return dct


# end of file
