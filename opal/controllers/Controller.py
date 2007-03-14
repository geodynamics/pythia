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


class Controller(object):


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


    def globalContext(self):
        return dict()


    def response(self, request):
        __pychecker__ = 'unusednames=request'
        raise NotImplementedError("class %r must override 'response'" % self.__class__.__name__)


    def decorateResponse(self, response, request):
        return


# end of file
