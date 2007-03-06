#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                              cig.web
#
# Copyright (c) 2006, California Institute of Technology
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#
#    * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#
#    * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#
#    * Neither the name of the California Institute of Technology nor
#    the names of its contributors may be used to endorse or promote
#    products derived from this software without specific prior
#    written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


import os, sys
from os.path import dirname, join

import Specfem3DGlobe
appTag = "Specfem3DGlobe"
webDir = join(dirname(Specfem3DGlobe.__file__), "web")
appDir = join(webDir, appTag)
appUrl = appTag.lower()
templateDir = join(appDir, "templates", appTag)


class Generator(object):

    def beginComponent(self, component): pass
    def endComponent(self, component): pass
    def onInventory(self, inventory): pass
    def onProperty(self, prop): pass

    def generate(self, components):
        self.begin()
        for component in components:
            self.visitComponent(component)
        self.end()

    def begin(self): pass

    def visitComponent(self, component):
        from pyre.inventory.Facility import Facility

        pyreInternalProps = ["help", "mode"]

        self.beginComponent(component)

        inventory = component.inventory
        self.onInventory(inventory)

        for prop in inventory._traitRegistry.itervalues():
            if isinstance(prop, Facility):
                continue
            if prop.name in pyreInternalProps or prop.name.startswith("help-"):
                continue
            self.onProperty(prop)

        self.endComponent(component)
        
        return

    def end(self): pass




class Debug(Generator):
    def beginComponent(self, component): print component.name
    def onProperty(self, prop): print "    ", prop.name, prop


from pyre.inventory.properties.Bool import Bool
from pyre.inventory.properties.Dimensional import Dimensional
from pyre.inventory.properties.Float import Float
from pyre.inventory.properties.Integer import Integer
from pyre.inventory.properties.String import String

propTypeMap = {
    Bool:         ('BooleanField', ''),
    Dimensional:  ('FloatField', 'max_digits=19, decimal_places=10'),
    Float:        ('FloatField', 'max_digits=19, decimal_places=10'),
    Integer:      ('IntegerField', ''),
    String:       ('CharField', 'maxlength=255'),
}

class Models(Generator):

    def __init__(self):
        self.stream = None
    
    def begin(self):
        self.stream = open(join(appDir, "models.py"), "w")
        print >> self.stream
        print >> self.stream, "from django.db import models"

    def beginComponent(self, component):
        print >> self.stream
        print >> self.stream, "class %s(models.Model):" % component.__class__.__name__

    def onProperty(self, prop):
        if not propTypeMap.has_key(prop.__class__):
            print >> self.stream, "    # skipped", prop.name, prop
            return
        varName = prop.name.replace('-', '_')
        modelClass, args = propTypeMap[prop.__class__]
        print >> self.stream, "    %s = models.%s(%s)" % (varName, modelClass, args)

    def end(self):
        self.stream.close()


class FormTemplate(Generator):
    
    def __init__(self):
        self.stream = None
    
    def beginComponent(self, component):
        self.stream = open(join(templateDir, component.name.lower() + "_form.html"), "w")
        print >> self.stream, '''
{% extends "''' + appTag + '''/base.html" %}

{% block content %}

<h1>''' +  component.__class__.__name__ + '''</h1>

{% if form.has_errors %}
<h2>Please correct the following error{{ form.error_dict|pluralize }}:</h2>
{% endif %}

<form method="post" action=".">
    <table border="0">
'''
        return

    def onProperty(self, prop):
        if not propTypeMap.has_key(prop.__class__):
            return
        varName = prop.name.replace('-', '_')
        if prop.__class__ == Bool:
            print >> self.stream, '''
        <tr>
            <td align="right" valign="top">{{ form.''' + varName + ''' }}</td>
            <td valign="top"><label for="id_''' + varName + '''">''' + prop.name + '''</label></td>
            <td valign="top">{% if form.''' + varName + '''.errors %}<span class=error>{{ form.''' + varName + '''.errors|join:", " }}</span>{% endif %}</td>
        </tr>'''
        else:
            print >> self.stream, '''
        <tr>
            <td align=right valign="top"><label for="id_''' + varName + '''">''' + prop.name + ''':</label></td>
            <td valign="top">{{ form.''' + varName + ''' }}</td>
            <td valign="top">{% if form.''' + varName + '''.errors %}<span class=error>{{ form.''' + varName + '''.errors|join:", " }}</span>{% endif %}</td>
        </tr>'''
        return


    def endComponent(self, component):
        print >> self.stream, '''
    </table>
    <p><input type="submit" value="Save" />
</form>
{% endblock %}'''
        return



class ConfirmDeleteTemplate(Generator):
    
    def beginComponent(self, component):
        stream = open(join(templateDir, component.name.lower() + "_confirm_delete.html"), "w")
        print >> stream, '''
{% extends "''' + appTag + '''/base.html" %}

{% block content %}

<h1>Delete ''' +  component.__class__.__name__ + '''</h1>

<form method="post" action=".">
    <p>Are you sure you want to delete ''' +  component.name.lower() + ''' {{ object.id }}?
    <p><input type="submit" value="Delete" />
</form>
{% endblock %}
'''
        stream.close()
        return


class ListTemplate(Generator):
    
    def __init__(self):
        self.stream = None
        self.fieldTd = None
    
    def beginComponent(self, component):
        self.stream = open(join(templateDir, component.name.lower() + "_list.html"), "w")
        print >> self.stream, '''
{% extends "''' + appTag + '''/base.html" %}

{% block content %}

<h1>''' +  component.__class__.__name__ + ''' List</h1>

{% if object_list %}
    <table border="0">
        <tr>
            <th align="left" valign="top">id</th>
            <th align="left" valign="top">actions</th>'''
        self.fieldTd = ""
        return

    def onProperty(self, prop):
        if not propTypeMap.has_key(prop.__class__):
            return
        columnHeader = prop.name.replace('-', ' ')
        varName = prop.name.replace('-', '_')
        print >> self.stream, '''            <th align="left" valign="top">''' + columnHeader + '''</th>'''
        self.fieldTd += '''
            <td valign="top">{{ object.''' + varName + ''' }}</td>'''        
        return


    def endComponent(self, component):
        print >> self.stream, '''
        </tr>

        {% for object in object_list %}
        <tr>
            <th valign="top">{{ object.id }}</th>
            <td valign="top"><a href="{{ object.id }}/">Edit</a> <a href="{{ object.id }}/delete/">Delete</a></td>''' + self.fieldTd + '''
        </tr>
        {% endfor %}

    </table>
{% else %}
    <p>You have no ''' + component.name.lower() + '''s.</p>
{% endif %}

<p><a href="create/">Create ''' + component.name.lower() + '''</a>

{% endblock %}'''
        return




def startapp():
    #from django.core.management import execute_manager
    #import settings
    #execute_manager(settings, ["manage.py", "startapp", appTag])
    os.makedirs(appDir)
    open(join(webDir, "__init__.py"), "w").close()
    open(join(appDir, "__init__.py"), "w").close()
    stream = open(join(appDir, "views.py"), "w")
    print >> stream, "# Create your views here."
    stream.close()


def generateBaseHtml():
    stream = open(join(templateDir, "base.html"), "w")
    print >> stream, '''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
    <link rel="stylesheet" href="style.css" />
    <title>{% block title %}''' + appTag + '''{% endblock %}</title>
</head>

<body>
    <div id="sidebar">
        {% block sidebar %}
        <ul>
            <li><a href="/''' + appUrl + '''/">Home</a></li>
        </ul>
        {% endblock %}
    </div>

    <div id="content">
        {% block content %}{% endblock %}
    </div>
</body>'''
    stream.close()


def generateHomeHtml(components):
    stream = open(join(templateDir, "home.html"), "w")
    print >> stream, '''
{% extends "''' + appTag + '''/base.html" %}

{% block content %}

<h1>Home</h1>

<ul>'''
    for component in components:
        print >> stream, '''
    <li><a href="''' + component.name.lower() + '''/">''' + component.__class__.__name__ + '''</a>'''
    print >> stream, '''
</ul>

{% endblock %}'''
    stream.close()


def generateUrlsPy(components):
    stream = open(join(appDir, "urls.py"), "w")
    print >> stream, '''

from django.conf.urls.defaults import *
from models import ''',
    classNames = [component.__class__.__name__ for component in components]    
    print >> stream, ', '.join(classNames)

    for component in components:
        className = component.__class__.__name__
        componentName = component.name.lower()
        url = '/' + appUrl + '/' + componentName + '/'
        print >> stream, '''
# %(className)s

%(componentName)s_list_detail_args = {
    'queryset': %(className)s.objects.all(),
    'allow_empty': True,
}

%(componentName)s_create_update_args = {
    'model': %(className)s,
    'post_save_redirect': '%(url)s',
    }

%(componentName)s_delete_args = {
    'model': %(className)s,
    'post_delete_redirect': '%(url)s',
    }

''' % locals()

    print >> stream, '''
# URLs

urlpatterns = patterns('',
    (r'^$', 'django.views.generic.simple.direct_to_template', { 'template': '%(appTag)s/home.html' }),'''  % { 'appTag': appTag }

    
    for component in components:
        componentName = component.name.lower()
        print >> stream, r'''
    (r'^%(componentName)s/$', 'django.views.generic.list_detail.object_list', %(componentName)s_list_detail_args),
    (r'^%(componentName)s/create/$', 'django.views.generic.create_update.create_object', %(componentName)s_create_update_args),
    (r'^%(componentName)s/(?P<object_id>\d+)/$', 'django.views.generic.create_update.update_object', %(componentName)s_create_update_args),
    (r'^%(componentName)s/(?P<object_id>\d+)/delete/$', 'django.views.generic.create_update.delete_object', %(componentName)s_delete_args),
''' % locals()
    print >> stream, '''
)'''
    stream.close()


def generate():
    from Specfem3DGlobe.Mesher import Mesher
    from Specfem3DGlobe.Model import Model as SpecfemModel
    from Specfem3DGlobe.Solver import Solver

    class Model(SpecfemModel): componentNames = [ "model" ]

    os.makedirs(templateDir)

    components = [Mesher('mesher'),
                  Model('model'),
                  Solver('solver'),
                  ]
    generatorClasses = [Models, FormTemplate, ConfirmDeleteTemplate, ListTemplate]

    for cls in generatorClasses:
        generator = cls()
        generator.generate(components)

    generateBaseHtml()
    generateHomeHtml(components)
    generateUrlsPy(components)


def main():
    startapp()
    generate()


main()

# end of file
