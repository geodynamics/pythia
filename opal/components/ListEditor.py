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


    def __init__(self, allow_empty=True, SubEditor=None, **kwds):
        super(ListEditor, self).__init__(**kwds)
        self.allow_empty = allow_empty
        self.SubEditor = SubEditor or self.ObjectEditor


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
            allow_empty = self.allow_empty,
            extra_context = self.context,
            )

    def getActions(self):
        return [self.Action('new', "New")]


# end of file
