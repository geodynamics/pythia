#!/usr/bin/env nemesis

from importlib import import_module
import inspect
import types
import argparse

class App():
    """Application to print help for Pyre components, including facilities and properties.
    """

    def main(self):
        """Application entry point.
        """
        args = self._parse_command_line()
        try:
            base = import_module(args.path)
            if base.__doc__:
                print(base.__doc__)
            else:
                print("No help available for module {:s}.".format(base.__name__))
            if args.short:
                return
            print()
        except ImportError:
            base = import_module(".".join(args.path.split(".")[:-1]))

        cls_name = args.path.split(".")[-1]
        if self._has_class(base, cls_name):
            cls_obj = getattr(base, cls_name)()
            if cls_obj.__doc__:
                print(f"class {cls_name}")
                print(cls_obj.__doc__)
            else:
                print("No help available for {:s}.".format(cls_name))
            if args.short:
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