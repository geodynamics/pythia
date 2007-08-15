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


    from ObjectEditor import ObjectEditor


    def __init__(self, **attrs):
        super(ListEditor, self).__init__(**attrs)
        self.allowEmpty = attrs.get('allowEmpty', True)
        self.SubEditor = attrs.get('SubEditor', self.ObjectEditor)


    def getView(self, request):
        action = request.GET.get('action')
        if action is None:
            response = self.getListView(request)
        elif action == 'new':
            response = self.genericCreateObject(
                request,
                self.Model,
                extra_context = self.getFormContext(request),
                post_save_redirect = self.parentURL,
                )
        else:
            self.unknownAction(action, request)
            response = self.getListView(request)
        return response


    def getListView(self, request):
        return self.genericObjectList(
            request,
            self.querySet(),
            allow_empty = self.allowEmpty,
            extra_context = self.context,
            )

    def getActions(self):
        return [self.Action('new', "New")]


# end of file
