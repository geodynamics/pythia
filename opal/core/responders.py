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


from opal import http


class Responder(object):

    def response(self, request):
        raise NotImplemented

    def isLeaf(self):
        return not hasattr(self, 'subResponder')

    def notFound(self):
        raise http.Http404



class ResponderChain(Responder):
    
    def __init__(self, *responders):
        self.responders = responders

    def response(self, request):
        return self.responders[0].response(request)

    def subResponder(self, name):
        for responder in self.responders:
            try:
                return responder.subResponder(name)
            except http.Http404:
                pass
        self.notFound()

chain = ResponderChain



class DirectoryResponder(Responder):

    def __init__(self, index, dct):
        self.index = index
        self.dct = dct

    def response(self, request):
        return self.index.response(request)

    def subResponder(self, name):
        try:
            responder = self.dct[name]
        except KeyError:
            self.notFound()
        return responder

directory = DirectoryResponder



class QueryDirectoryResponder(Responder):

    def __init__(self, Model, Inquirer, subResponderFactory):
        self.Model = Model
        self.Inquirer = Inquirer
        self.subResponderFactory = subResponderFactory
        return

    def subResponder(self, name):
        from opal.core.exceptions import ObjectDoesNotExist
        query = self.newQuery(name)
        try:
            obj = query.get(self.Model._default_manager.all())
        except ObjectDoesNotExist:
            raise http.Http404("No %s found matching the query '%s'." % (self.Model._meta.verbose_name, query))
        return self.newSubResponder(obj)

    def newQuery(self, key):
        return self.Inquirer.newQuery(key)
   
    def newSubResponder(self, obj):
        return self.subResponderFactory(obj)

queryDirectory = QueryDirectoryResponder



class FunctionResponder(Responder):

    def __init__(self, function, *args, **kwds):
        self.function = function
        self.args = args
        self.kwds = kwds

    def response(self, request):
        return self.function(request, *self.args, **self.kwds)



class MethodResponderContext(Responder):

    def __init__(self, instance, method, *args, **kwds):
        self.instance = instance
        self.method = method
        self.args = args
        self.kwds = kwds

    def response(self, request):
        return self.method(self.instance, request, *self.args, **self.kwds)



class MethodResponder(Responder):

    def __init__(self, method, instance):
        self.method = method
        self.instance = instance

    def response(self, request):
        return self.method(self.instance, request)

    def __call__(self, *args, **kwds):
        return MethodResponderContext(self.instance, self.method, *args, **kwds)



class ResponderMethodDescriptor(object):

    def __init__(self, method):
        self.method = method

    def __get__(self, instance, cls=None):
        return MethodResponder(self.method, instance)

respondermethod = ResponderMethodDescriptor



class Redirector(Responder):

    def __init__(self, newUrl):
        self.newUrl = newUrl

    def response(self, request):
        return http.HttpResponsePermanentRedirect(self.newUrl)



# end of file
