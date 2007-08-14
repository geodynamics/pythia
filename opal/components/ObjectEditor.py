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


from Editor import Editor


class ObjectEditor(Editor):


    def __init__(self, **attrs):
        super(ObjectEditor, self).__init__(**attrs)
        self.model = attrs['model']


    def getView(self, request):
        from django.views.generic.create_update import delete_object, update_object
        id = self.model.id
        action = request.GET.get('action')
        if action is None:
            response = self.getDetailView(request)
        elif action == 'edit':
            response = update_object(request, self.Model,
                                     object_id = id,
                                     extra_context = self.getFormContext(request),
                                     )
        elif action == 'delete':
            response = delete_object(request, self.Model, self.parentURL,
                                     object_id = id,
                                     extra_context = self.getFormContext(request),
                                     )
        else:
            self.unknownAction(action, request)
            response = self.getDetailView(request)
        return response


    def getDetailView(self, request):
        from django.views.generic.list_detail import object_detail
        return object_detail(request, self.querySet(),
                             object_id = self.model.id,
                             extra_context = self.context,
                             )


    def getActions(self):
        return [Action('edit', "Edit"), Action('delete', "Delete")]


# end of file
