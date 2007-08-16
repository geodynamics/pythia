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


from Controller import Controller
from opal.http import HttpResponseRedirect


class DeletionController(Controller):
    """
    Generic object-deletion controller.

    The given template will be used to confirm deletetion if the view is
    fetched using GET; for safty, deletion will only be performed if the
    method is POST.

    Templates: ``<app_label>/<model_name>_confirm_delete.html``
    Context:
        object
            the original object being deleted
    """


    templateNameTag = "confirm_delete"


    def __init__(self, post_redirect=None, **kwds):
        Controller.__init__(self, **kwds)
        self.post_redirect = post_redirect


    def response(self, request):

        if request.method == "POST":
            self.view.obj.delete()
            if request.user.is_authenticated():
                request.user.message_set.create(message="The %s was deleted." % self.model._meta.verbose_name)
            return HttpResponseRedirect(self.post_redirect)

        return super(DeletionController, self).response(request)


# end of file
