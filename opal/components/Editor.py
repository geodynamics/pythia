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


from WebComponent import WebComponent


class Action(object):
    def __init__(self, slug, name):
        self.slug = slug
        self.name = name


class Editor(WebComponent):


    Action = Action


    def __init__(self, **attrs):
        super(Editor, self).__init__(**attrs)
        self.Model = attrs['Model']
        self.manager = self.Model.objects
        self.context['actions'] = self.getActions()


    def querySet(self):
        return self.manager.all()


    def createSubcomponent(self, slug, **attrs):
        attrs['slug'] = slug
        attrs['url'] = self.url
        attrs['Model'] = self.Model
        model = attrs['model']
        attrs['title'] = model.name
        c = self.SubEditor(**attrs)
        return c


    def subcomponent(self, slug, **attrs):
        try:
            model = self.manager.get(slug = slug)
        except self.Model.DoesNotExist:
            raise self.Http404
        return self.createSubcomponent(slug, model=model, **attrs)


    def expand(self, **attrs):
        if self.subcomponents is None:
            self.subcomponents = {}
            for model in self.querySet():
                slug = model.slug
                self.subcomponents[slug] =  self.createSubcomponent(slug, model=model, **attrs)
        return self.subcomponents


    def getFormContext(self, request):
        context = dict(self.context)
        context['actionURL'] = request.get_full_path()
        return context


    def getActions(self):
        return []


    def unknownAction(self, action, request):
        self.postMessage("Unknown action '%s'." % action, request)
        return


# end of file
