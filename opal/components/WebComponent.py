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
import opal.views as views
import opal.controllers as controllers

from opal.template import Context, RequestContext, loader
from opal import http

class WebComponent(Component):


    models = []
    urlpatterns = []


    # urlpatterns support

    include = lambda urlconf_module: [urlconf_module]

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

    def genericObjectList(request, **kwds):
        view = views.ListView(**kwds)
        return view.response(request)


    def genericObjectDetail(request, **kwds):
        view = views.DetailView(**kwds)
        return view.response(request)


    # generic views -- CRUD

    def genericCreateObject(request, post_save_redirect=None, follow=None, **kwds):
        controller = controllers.CreationController(
            post_redirect = post_save_redirect,
            follow = follow,
            )
        view = views.DetailView(controller = controller, **kwds)
        return view.response(request)


    def genericUpdateObject(request, post_save_redirect=None, follow=None, **kwds):
        controller = controllers.UpdateController(
            post_redirect = post_save_redirect,
            follow = follow,
            )
        view = views.DetailView(controller = controller, **kwds)
        return view.response(request)


    def genericDeleteObject(request, post_delete_redirect, **kwds):
        controller = controllers.DeletionController(
            post_redirect = post_delete_redirect,
            )
        view = views.DetailView(controller = controller, **kwds)
        return view.response(request)


    # errors

    def handler404(request, template_name='404.html'):
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


    def handler500(request, template_name='500.html'):
        """
        500 error handler.

        Templates: `500.html`
        Context: None
        """
        t = loader.get_template(template_name) # You need to create a 500.html template.
        return http.HttpResponseServerError(t.render(Context({})))


# end of file
