import sys
import copy
import enum

from typing import NamedTuple


class Flags(enum.IntFlag):
    Single = 2
    Multiple = 4


Input = NamedTuple(
    "Input", (
        ("qname", str),
        ("description", str),
        ("type", str),
        ("cardinality", 'Tuple[int, int]'),
        ("replaces", 'List[str]'),
    )
)
Input.__new__.__defaults__ = ((0, 1), [])


class Input(Input):
    """
    Attributes
    ----------
    qname: str
        Qualified name for the input. This uniquely identifies the input slot
        *within* the node.

    display_name: str
        Short human readable name.

    description : str
        A longer description of the input (for human consumption).

    type: str
        A string representation of the type.

    resolved_type: Union[type, Tuple[type], abc.ABC, None]
        Resolved type if available.

    cardinality: Tuple[int, int]
        Default 0,1

    replaces: List[str]
        Deprecated.
    """


Output = NamedTuple(
    "Output", (
        ("qname", str),
        ("description", str),
        ("type", str),
        ("cardinality", "Tuple[int, int]"),
        ("replaces", 'List[str]'),
    )
)


class Output(Output):
    """
    """
    pass


class NodeMeta:
    inputs = ()  # type: Tuple[Input]
    outputs = ()  # type: Tuple[Output]
    qname = ...  # type: str
    name = ...   # type: str

    description = ...
    project_name = ...

    keywords = ...
    priority = ...
    icon = ...  # type: Union[str, QIcon]
    #: A qname of a NodeGraphicsItem factory
    display_delegate = ...          # type: str
    #: A qname of a QWidget factory
    display_control_delegate = ...  # type: str


class Category(NamedTuple):
    # single defining top level namespace
    qname: str = ...
    # human readable display name
    name: str = ...
    description: str = ""
    long_description: str = ""
    # prefered display color for the category and its nodes
    display_color: str = ""
    # Is this category (by default) hidden in the GUI.
    hidden: bool = False
