"""Formatters for help information used in Configurable showComponents() and showProperties().
"""

class Ascii(object):
    """Plain ASCII text.
    """

    @staticmethod
    def formatComponents(name, facilities):
        """Format components information.

        name: Facility name.
        facilities: Dictionary with facilities information.
          - name: Name of facility
          - doc: Facility help string.
          - descriptor: Descriptor for facility.
        """
        print("facilities of %r:" % name)
        for facility in facilities:
            print("    %s=<component name>: %s" % (facility["name"], facility["doc"]))
            value = facility["descriptor"].value
            locator = facility["descriptor"].locator
            print("        current value: %r, from %s" % (value.name, locator))
            print("        configurable as: %s" % ", ".join(value.aliases))

    @staticmethod
    def formatProperties(name, properties):
        """Format properties information.

        name: Facility name.
        properties: Dictionary with properties information.
          - name: Name of property
          - doc: Property help string
          - trait: Property trait
          - descriptor: Descriptor for property
        """
        print("properties of %r:" % name)
        for prop in properties:
            trait = prop["trait"]
            value = prop["descriptor"].value
            locator = prop["descriptor"].locator
            print("    %s=<%s>: %s" % (prop["name"], trait.type, prop["doc"]))
            print("        default value: %r" % trait.default)
            print("        current value: %r, from %s" % (value, locator))
            if trait.validator:
                print("        validator: %s" % trait.validator)


class MarkdownMyST(object):
    """Markedly structured text flavored Markdown.
    """

    @staticmethod
    def formatComponents(name, facilities):
        """Format components information.

        name: Facility name.
        facilities: Dictionary with facilities information.
          - name: Name of facility
          - doc: Facility help string.
          - descriptor: Descriptor for facility.
        """
        for facility in facilities:
            print("* `%s`: %s" % (facility["name"], facility["doc"]))
            value = facility["descriptor"].value
            locator = facility["descriptor"].locator
            print("  - **current value**: %r, from %s" % (value.name, locator))
            print("  - **configurable as**: %s" % ", ".join(value.aliases))

    @staticmethod
    def formatProperties(name, properties):
        """Format properties information.

        name: Facility name.
        properties: Dictionary with properties information.
          - name: Name of property
          - trait: Property trait
          - doc: Property help string
          - descriptor: Descriptor for property
        """
        for prop in properties:
            trait = prop["trait"]
            value = prop["descriptor"].value
            locator = prop["descriptor"].locator
            print("* `%s`=\<%s\>: %s" % (prop["name"], trait.type, prop["doc"]))
            print("  - **default value**: %r" % trait.default)
            print("  - **current value**: %r, from %s" % (value, locator))
            if trait.validator:
                print("  - **validator**: %s" % trait.validator)
