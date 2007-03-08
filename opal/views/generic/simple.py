from opal.shortcuts import render_to_response
from opal.template import RequestContext
from opal.http import HttpResponse, HttpResponsePermanentRedirect, HttpResponseGone

def direct_to_template(request, template, **kwargs):
    """
    Render a given template with any extra URL parameters in the context as
    ``{{ params }}``.
    """
    return render_to_response(template, {'params' : kwargs}, context_instance=RequestContext(request))

def redirect_to(request, url, **kwargs):
    """
    Redirect to a given URL.

    The given url may contain dict-style string formatting, which will be
    interpolated against the params in the URL.  For example, to redirect from
    ``/foo/<id>/`` to ``/bar/<id>/``, you could use the following URLconf::

        urlpatterns = patterns('',
            ('^foo/(?p<id>\d+)/$', 'opal.views.generic.simple.redirect_to', {'url' : '/bar/%(id)s/'}),
        )

    If the given url is ``None``, a HttpResponseGone (410) will be issued.
    """
    if url is not None:
        return HttpResponsePermanentRedirect(url % kwargs)
    else:
        return HttpResponseGone()