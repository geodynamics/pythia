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


from FormController import FormController
from opal.core.xheaders import populate_xheaders


class UpdateController(FormController):
    """
    Generic object-update controller.

    Templates: ``<app_label>/<model_name>_form.html``
    Context:
        form
            the form wrapper for the object
        object
            the original object being edited
    """


    templateNameTag = "form"

    
    def newManipulator(self):
        model = self.view.model
        return self.model.ChangeManipulator(getattr(model, model._meta.pk.name), follow=self.follow)


    def successMessage(self):
        return "The %s was updated successfully." % self.model._meta.verbose_name


    def decorateResponse(self, response, request):
        super(UpdateController, self).decorateResponse(response, request)
        model = self.view.model
        populate_xheaders(request, response, self.model, getattr(model, model._meta.pk.name))
        return


# end of file
