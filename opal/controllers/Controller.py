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


Responder = object


class Controller(Responder):


    def __init__(self):
        self._view = None
        self.model = None


    def _getView(self):
        return self._view
    def _setView(self, view):
        import weakref
        self._view = weakref.proxy(view)
        self.model = view.model
    view = property(_getView, _setView)


    def _getTemplateNameTag(self):
        return self.view.defaultTemplateNameTag
    templateNameTag = property(_getTemplateNameTag)


    def contextDictionary(self, request):
        return dict()


    def response(self, request):
        response = self.view.response(request)
        self.decorateResponse(response, request)
        return response


    def decorateResponse(self, response, request):
        return


# end of file
