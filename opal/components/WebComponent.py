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


from pyre.components import Component
from pyre.inventory.ConfigurableClass import ConfigurableClass
import opal.views as views
import opal.controllers as controllers

from opal.template import Context, RequestContext, loader
from opal import http


class Property(object):
    def __init__(self, **attrs):
        self.__dict__.update(attrs)


component = Property


class WebComponentClass(ConfigurableClass):


    def __init__(Class, name, bases, dct):
        ConfigurableClass.__init__(Class, name, bases, dct)

        subcomponentRegistry = {}

        for name, prop in [kv for kv in dct.iteritems()
                           if isinstance(kv[1], Property)]:
            slug = prop.attrs.setdefault('slug', name)
            subcomponentRegistry[slug] = prop

        Class.subcomponentRegistry = subcomponentRegistry

        return


class WebComponent(Component):


    models = []
    urlpatterns = []


    # urlpatterns support

    def include(self, urlconf_module):
        return [urlconf_module]


    def patterns(self, *tuples):
        from opal.core.urlresolvers import RegexURLPattern, RegexURLResolver
        pattern_list = []
        for t in tuples:
            regex, view_or_include = t[:2]
            default_kwargs = t[2:]
            if type(view_or_include) == list:
                include = view_or_include[0]
                pattern_list.append(RegexURLResolver(regex, include, *default_kwargs))
            else:
                view = view_or_include
                pattern_list.append(RegexURLPattern(regex, view, *default_kwargs))
        return pattern_list


    # generic views

    def genericObjectList(self, request, queryset, **kwds):
        view = views.ListView(queryset = queryset, **kwds)
        controller = view.controller
        return controller.response(request)


    def genericObjectDetail(self, request, queryset, query, **kwds):
        # NYI: Unlike Django's object_detail() function, this discards
        # 'queryset'.  This may not be appropriate, even though this
        # is a view of a single object: e.g., if the queryset is a
        # per-user query, then perhaps 'Http404' should be raised.
        # OTOH, in Django's create_update functions (replicated in the
        # CRUD stuff below), 'model' seems to be good enough; which
        # begs the question as to why this method doesn't take a
        # 'model' instead of a 'queryset'.
        model = queryset.model
        view = views.DetailView(model, query, **kwds)
        controller = view.controller
        return controller.response(request)


    # generic views -- CRUD

    def genericCreateObject(self, request, model, post_save_redirect=None, follow=None, **kwds):
        controller = controllers.CreationController(
            post_redirect = post_save_redirect,
            follow = follow,
            )
        view = views.DetailView(model, None, controller = controller, **kwds)
        return controller.response(request)


    def genericUpdateObject(self, request, model, query, post_save_redirect=None, follow=None, **kwds):
        controller = controllers.UpdateController(
            post_redirect = post_save_redirect,
            follow = follow,
            )
        view = views.DetailView(model, query, controller = controller, **kwds)
        return controller.response(request)


    def genericDeleteObject(self, request, model, query, post_delete_redirect, **kwds):
        controller = controllers.DeletionController(
            post_redirect = post_delete_redirect,
            )
        view = views.DetailView(model, query, controller = controller, **kwds)
        return controller.response(request)


    # errors

    def handler404(self, request, template_name='404.html'):
        """
        Default 404 handler, which looks for the requested URL in the redirects
        table, redirects if found, and displays 404 page if not redirected.

        Templates: `404.html`
        Context:
            request_path
                The path of the requested URL (e.g., '/app/pages/bad_page/')
        """
        t = loader.get_template(template_name) # You need to create a 404.html template.
        return http.HttpResponseNotFound(t.render(RequestContext(request, {'request_path': request.path})))


    def handler500(self, request, template_name='500.html'):
        """
        500 error handler.

        Templates: `500.html`
        Context: None
        """
        t = loader.get_template(template_name) # You need to create a 500.html template.
        return http.HttpResponseServerError(t.render(Context({})))


    #------------------------------------------------------------------------
    # unearthed stuff


    __metaclass__ = WebComponentClass


    #from cig.web.views import View
    from opal.http import Http404


    def __xinit__(self, **attrs):
        super(WebComponent, self).__init__()
        self.slug = attrs.get('slug')
        self.context = attrs.get('context', {})
        self.parentURL = attrs.get('url')
        self.subcomponents = None
        self._initTreeNode(**attrs)


    def createSubcomponent(self, slug, **attrs):
        prop = self.subcomponentRegistry[slug]
        attrs.update(prop.attrs)
        attrs['slug'] = slug
        attrs['url'] = self.url
        Class = attrs['Class']
        c = Class(**attrs)
        return c


    def subcomponent(self, slug, **attrs):
        self.expand(**attrs)
        try:
            c = self.subcomponents[slug]
        except KeyError:
            raise self.Http404
        return c


    def iterSubcomponents(self):
        self.expand()
        for c in self.subcomponents.itervalues():
            yield c
        return


    def expand(self, **attrs):
        if self.subcomponents is None:
            self.subcomponents = {}
            for slug in self.subcomponentRegistry.iterkeys():
                self.subcomponents[slug] =  self.createSubcomponent(slug, **attrs)
        return self.subcomponents


    def resolve(self, path, **attrs):
        context = attrs.setdefault('context', {})
        context.setdefault('root', self)
        item = path[0]
        path = path[1:]
        if item:
            subcomponent = self.subcomponent(item, **attrs)
            self.selectedChild = subcomponent
            return subcomponent.resolve(path, **attrs)
        if path:
            raise self.Http404
        self.isExpanded = True
        args = ()
        kwargs = {}
        #return self.View(component=self), args, kwargs
        return self.getView, args, kwargs


    # TreeNode protocol

    def _initTreeNode(self, **attrs):
        # this node
        self.name = attrs.get('name', self.slug)
        self.title = attrs.get('title', self.name.title())
        self.url = attrs['url'] + '/' + self.slug

        # children
        self.isLeaf = False
        self.isExpanded = False
        self.selectedChild = None


    def _getChildren(self):
        return [child for child in self.iterChildren()]
    children = property(_getChildren)


    def iterChildren(self):
        for component in self.iterSubcomponents():
            yield component
        return


    def postMessage(self, message, request):
        request.user.message_set.create(message = message)
        return


# end of file
