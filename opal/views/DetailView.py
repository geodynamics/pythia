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


    def __init__(self, model, template_name_field=None, **kwds):
        View.__init__(self, model, **kwds)
        self.template_name_field = template_name_field
        return


    def loadTemplate(self):
        if self.model and self.template_name_field:
            template_name_list = [getattr(self.model, self.template_name_field), self.template_name]
            t = self.template_loader.select_template(template_name_list)
        else:
            t = super(DetailView, self).loadTemplate()
        return t


    def contextDictionary(self, request):
        dct = super(DetailView, self).contextDictionary(request)
        if self.model:
            dct[self.template_object_name] = self.model
        return dct


# end of file
