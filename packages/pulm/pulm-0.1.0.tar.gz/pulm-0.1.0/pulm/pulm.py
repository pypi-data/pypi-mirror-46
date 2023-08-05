#!/usr/bin/env python

import argparse

import os
import textwrap
from abc import abstractmethod, ABC


class Parser(ABC):
    """ Parser of components. """

    def __init__(self, entry):
        self._entry = entry

    @staticmethod
    def get_parser(entry_path):

        if os.path.isdir(entry_path):
            parser = ModuleParser(entry_path)
        else:
            parser = FileParser(entry_path)

        return parser

    def parse_components(self):
        pass


class ModuleParser(Parser):
    """ Parse components in a module """

    def __init__(self, entry):
        super().__init__(entry)

    def parse_components(self):
        components = []
        for entry in os.listdir(self._entry):
            entry_path = os.path.join(self._entry, entry)
            entry_parser = Parser.get_parser(entry_path)
            components.extend(entry_parser.parse_components())

        return components


class FileParser(Parser):
    """ Parse components (classes) in a file"""

    def __init__(self, entry):
        super().__init__(entry)

    def parse_components(self):

        # Only managing python file for now
        if not self._entry.endswith(".py"):
            return []

        with open(file=self._entry, mode="r") as fd:
            text = fd.read()

            class_blocks = text.split("\nclass ")
            if "import " in class_blocks[0]:
                class_blocks = class_blocks[1:]

            # TODO : resolve this
            if len(class_blocks) > 1 and  "if __name__ == __main__" in class_blocks[-1]:
                class_blocks = class_blocks[:-2]

            classes = list(map(self._parse_class_block, class_blocks))

        return classes

    def _parse_class_block(self, block):
        """
        Return a Class object from a block of code.

        :param block: block of code (without the "class" keyword)
        :return:
        """

        lines = block.split("\n")
        name_class = lines[0].replace(":", "").strip()
        upper_class = None

        if "(" in name_class:
            tokens = name_class.split("(")
            name_class = tokens[0]
            upper_class = tokens[1].split(")")[0]

        methods = block.split("def ")

        del methods[0]

        public_methods = []
        private_methods = []

        public_attributes, private_attributes = [], []
        for method in methods:
            method_signature = method.split(")")[0].strip() + ")"
            if "__init__" == method_signature:
                public_attributes, private_attributes = self._parse_init_block(method)

            if method_signature[0] == "_" and method_signature[1] != "_":
                private_methods.append(method_signature[1:])
            else:
                public_methods.append(method_signature)

        clazz = Class(name_class, upper_class, public_attributes, public_methods, private_attributes, private_methods)

        return clazz

    def _parse_init_block(self, block):
        """
        Gather class attributes of a class using a block of code.

        :param block: the block of code of the __init__ method (without the "def" keyword)
        :return: list of public and private attributes names
        """

        lines = block.split("\n")

        private_attributes = []
        public_attributes = []

        for line in lines:
            if "self." in line:
                attribute_name = line.replace("self.", "").split("=")[0].strip()
                if attribute_name[0] == "_" and attribute_name[1] != "_":
                    private_attributes.append(attribute_name[1:])
                else:
                    public_attributes.append(attribute_name)

        return public_attributes, private_attributes


class Composite(ABC):
    """ A wrapper of Components.

    A Composite can also be a Component.

    Used to recursively construct the plant-uml script information.
    """

    def __init__(self, name):
        self._name = name
        self._components = {}
        self._indentation = ""

    def register_components(self, components):
        assert len(set(components).intersection(self._components.keys())) == 0
        for compo in components:
            self._components[compo._name] = compo

    def __repr__(self):
        str_repr = self._header()

        for component_name, component in self._components.items():
            str_repr += textwrap.indent(str(component), self._indentation)

        str_repr += self._footer()

        return str_repr

    @abstractmethod
    def _header(self):
        pass

    @abstractmethod
    def _footer(self):
        pass


class Class(object):
    """ Wrapper of a python class.

    A component only.
    """

    def __init__(self, name, upper_class, public_attributes, public_methods, private_attributes, private_methods):
        self._name = name
        self._upper_class = upper_class
        self._public_attributes = public_attributes
        self._public_methods = public_methods

        self._private_attributes = private_attributes
        self._private_methods = private_methods

    def __repr__(self):
        if self._name == "":
            return ""

        str_repr = "\n"
        str_repr += "class %s { \n" % self._name

        for pa in self._public_attributes:
            str_repr += f"  + {pa}\n"

        for pa in self._private_attributes:
            str_repr += f"  - {pa}\n"

        for pm in self._public_methods:
            str_repr += f"  + {pm}\n"

        for pm in self._private_methods:
            str_repr += f"  - {pm}\n"

        str_repr += "}\n"

        if self._upper_class is not None:
            str_repr += f"\n{self._name} --|> {self._upper_class}\n"

        str_repr += "\n"
        return str_repr


class Scope(Composite):
    """ The given scope of the project.

    Produces a plant-uml script when getting the string representation of it.

    Is the base Composite.
    """

    def __init__(self, name):
        super().__init__(name)
        self._custom_headers = []

    def register_custom_headers(self, headers):
        self._custom_headers.extend(headers)

    def _header(self):
        """
        Print the header of the plant-uml script

        :return:
        """
        str_repr = "@startuml\n\n"

        for custom_header in self._custom_headers:
            str_repr += custom_header

        str_repr += f"\ntitle {self._name}\n"

        return str_repr

    def _footer(self):
        """
        Print the footer of the plant-uml script

        :return:
        """
        str_repr = "\n@enduml\n"
        return str_repr


class Module(Composite):
    """ Composite for a module (ie a set of Classes or Modules) """

    def __init__(self, name):
        super().__init__(name)

        self._indentation = "  "

    def _header(self):
        """
        Print the header of the plantuml script

        :return:
        """
        str_repr = "\npackage %s {\n\n" % self._name

        return str_repr

    def _footer(self):
        """
        Print the footer of the plantuml script

        :return:
        """
        str_repr = "\n}\n"
        return str_repr


if __name__ == "__main__":

    default_title = "Class Diagram for {path}"
    argparser = argparse.ArgumentParser(description='Evaluate a model using a serialized version of it.')

    argparser.add_argument('--path', metavar='path',
                           type=str, required=True,
                           help=f'the file or module to generate UML for.')

    argparser.add_argument('--font', metavar='font',
                           type=str, required=False,
                           help=f'the font to use for.')

    argparser.add_argument('--title', metavar='title',
                           type=str, required=False,
                           default=default_title,
                           help=f'the title to use for the project.')

    args = argparser.parse_args()

    to_parse_path = args.path
    title = args.title
    font = args.font

    custom_headers = list()

    if font:
        custom_headers.append(f"skinparam classFontName {args.fonts}\n")

    if title == default_title:
        basename_path = to_parse_path.split(os.sep)[-1]
        title = title.format(path=basename_path)

    parser = Parser.get_parser(to_parse_path)
    components = parser.parse_components()

    # Zipping it
    landscape = Scope(title)
    landscape.register_components(components)

    landscape.register_custom_headers(custom_headers)

    print(landscape)
