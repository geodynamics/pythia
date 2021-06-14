# ----------------------------------------------------------------------
#
# Brad T. Aagaard, U.S. Geological Survey
#
# This code was developed as part of the Computational Infrastructure
# for Geodynamics (http://geodynamics.org).
#
# Copyright (c) 2010-2021 University of California, Davis
#
# ----------------------------------------------------------------------
"""Python module for operations related to the Pyre component hierarchy.
"""

def getComponentFromPath(parent, path):
    """Get component at path in Pyre hierarchy relative to parent.

    Args:
        parent (object)
            Parent object
        path (str)
            Relative path to object (for example "parent.child.subchild").
    Returns (object):
        Object at given path.
    """
    tree = path.split(".")
    obj = parent
    for name in tree:
        try:
            obj = obj.getTraitValue(name)
        except AttributeError as err:
            obj.showComponents()
            raise AttributeError(f"Could not find '{name}' in hierarchy path '{path}'." \
                f"See '{obj.name}' components above.")
    return obj


# End of file
