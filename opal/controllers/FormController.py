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
from opal import forms
from opal.core.exceptions import ImproperlyConfigured
from opal.http import HttpResponseRedirect


class FormController(Controller):


    templateNameTag = "form"


    def __init__(self, post_redirect=None, follow=None, **kwds):
        Controller.__init__(self, **kwds)
        self.post_redirect = post_redirect
        self.follow = follow
        self.data = None
        self.errors = {}


    def createGlobalContext(self):
        context = dict()
        form = self.newFormWrapper()
        context['form'] = form
        return context


    def newFormWrapper(self):
        return forms.FormWrapper(self.manipulator, self.data, self.errors)


    def getData(self, request):
        method = request.method
        if method == "POST":
            # If data was POSTed, we're trying to create a new object
            self.getPostedData(request)
        elif method == "GET":
            # No POST, so we want a brand new form without any data or errors
            self.getBlankData(request)
        else:
            raise ValueError("unknown method: '%s'" % method)


    def getPostedData(self, request):
        from opal.db.models import FileField
        data = request.POST.copy()
        self.data = data
        if self.model._meta.has_field_type(FileField):
            data.update(request.FILES)
        # Check for errors
        self.errors = self.manipulator.get_validation_errors(data)
        self.manipulator.do_html2python(data)


    def getBlankData(self, request):
        __pychecker__ = 'unusednames=request'
        # This makes sure the form acurately represents the fields of the place.
        self.data = self.manipulator.flatten_data()


    def response(self, request):
        self.manipulator = self.newManipulator()
        self.getData(request)
        
        if request.method != "POST" or self.errors:
            # Let the view respond to this request.
            return self.view.render(request)

        # POST with no errors -- this means we can save the data!
        obj = self.manipulator.save(self.data)

        if request.user.is_authenticated():
            request.user.message_set.create(message=self.successMessage())

        # Do a post-after-redirect so that reload works, etc.
        # Redirect to the new object: first by trying post_redirect,
        # then by obj.get_absolute_url; fail if neither works.
        if self.post_redirect:
            redirect_to = self.post_redirect % obj.__dict__
        elif hasattr(obj, 'get_absolute_url'):
            redirect_to = obj.get_absolute_url()
        else:
            raise ImproperlyConfigured("No URL to redirect to.")

        return HttpResponseRedirect(redirect_to)


    def newManipulator(self):
        raise NotImplementedError()


    def successMessage(self):
        raise NotImplementedError()


# end of file
