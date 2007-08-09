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


class Query(object):

    def __init__(self, fieldName, key):
        self.fieldName = fieldName
        self.key = key

    def apply(self, queryset):
        return queryset.filter(**{self.fieldName: self.key})

    def get(self, queryset):
        queryset = self.apply(queryset)
        return queryset.get()

    def __str__(self):
        return "%s='%s'" % (self.fieldName, self.key)



class Inquirer(object):

    Query = Query
    
    def newQuery(self, key):
        return self.Query(self.fieldName, key)

    def __init__(self, fieldName):
        self.fieldName = fieldName


primaryInquirer = Inquirer('pk')


# end of file
