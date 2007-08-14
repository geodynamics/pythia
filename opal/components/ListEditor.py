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


class ListEditor(Editor):


    def __init__(self, **attrs):
        super(ListEditor, self).__init__(**attrs)
        self.allowEmpty = attrs.get('allowEmpty', True)
        self.SubEditor = attrs.get('SubEditor', ObjectEditor)


    def getView(self, request):
        from django.views.generic.create_update import create_object
        action = request.GET.get('action')
        if action is None:
            response = self.getListView(request)
        elif action == 'new':
            response = create_object(request, self.Model,
                                     extra_context = self.getFormContext(request),
                                     post_save_redirect = self.parentURL,
                                     )
        else:
            self.unknownAction(action, request)
            response = self.getListView(request)
        return response


    def getListView(self, request):
        from django.views.generic.list_detail import object_list
        return object_list(request, self.querySet(),
                           allow_empty = self.allowEmpty,
                           extra_context = self.context,
                           )

    def getActions(self):
        return [Action('new', "New")]


# end of file
