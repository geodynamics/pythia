# This module is DEPRECATED!
#
# You should no longer be pointing your mod_python configuration
# at "opal.core.handler".
#
# Use "opal.core.handlers.modpython" instead.

from opal.core.handlers.modpython import ModPythonHandler

def handler(req):
    return ModPythonHandler()(req)
