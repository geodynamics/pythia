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


class CreationController(FormController):
    """
    Generic object-creation controller.

    Templates: ``<app_label>/<model_name>_form.html``
    Context:
        form
            the form wrapper for the object
    """


    def newManipulator(self):
        return self.model.AddManipulator(follow=self.follow)


    def successMessage(self):
        return "The %s was created successfully." % self.model._meta.verbose_name


# end of file
