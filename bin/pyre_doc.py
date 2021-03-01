#!/usr/bin/env nemesis

from importlib import import_module
import inspect
import types
import argparse

class App():
    """Application to print help for Pyre components, including facilities and properties.
    """

    def __init__(self):
        self.short = False
        self.mod = None

    def main(self):
        """Application entry point.
        """
        args = self._parse_command_line()
        self.short = args.short
        try:
            self.mod = import_module(args.path)
            self._module_doc()
            if self.short:
                return
            print()
        except ImportError:
            # User specified a class within a module.
            self.mod = import_module(".".join(args.path.split(".")[:-1]))
        cls_name = args.path.split(".")[-1]
        if App._has_class(self.mod, cls_name):
            self._class_doc(cls_name)
        
    def _module_doc(self):
        """Show documentation for module."""
        if self.mod.__doc__:
            print(self.mod.__doc__)
        else:
            print("No help available for module {:s}.".format(self.mod.__name__))

    def _class_doc(self, cls_name):
        """Show documentation for class with name cls_name in module."""
        cls_obj = getattr(self.mod, cls_name)()
        if cls_obj.__doc__:
            print(f"class {cls_name}")
            print(cls_obj.__doc__)
        else:
            print("No help available for class {:s}.".format(cls_name))
        if self.short:
            return

        if App._has_function(cls_obj, "showComponents"):
            cls_obj.showComponents()
        if App._has_function(cls_obj, "showProperties"):
            cls_obj.showProperties()

    def _parse_command_line(self):
        """Parse command line arguments.
        """
        description = "Show help for module or object at a given path. If path is for a module, show help " \
            "for class of same name. If the object is a Pyre component, then show Pyre facilities and properties."
        parser = argparse.ArgumentParser(description=description)
        parser.add_argument("path", metavar="OBJECT", type=str, 
            help="Path to module or object for help.")
        parser.add_argument("--short", action="store_true", dest="short", default=False,
            help="Only show help for module or object at path. Do not show Pyre components or properties.")
        return parser.parse_args()

    @staticmethod
    def _has_function(obj, name):
        """Return True if obj has function name."""
        return hasattr(obj, name) and type(inspect.getattr_static(obj, name)) == types.FunctionType

    @staticmethod
    def _has_class(obj, name):
        """Return True if obj has class name."""
        return hasattr(obj, name) and inspect.isclass(inspect.getattr_static(obj, name))


if __name__ == "__main__":
    App().main()