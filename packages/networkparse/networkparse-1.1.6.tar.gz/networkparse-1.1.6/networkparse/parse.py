"""
Parse a network configuration file

To begin using `networkparse`, typically an subclass of :class:`~ConfigBase` will be
instantiated with the text of the configuration file. Currently, `networkparse` has
support for:

- Cisco IOS: :class:`~ConfigIOS`
- Cisco NX-OS: :class:`~ConfigNXOS`
- Fortinet: :class:`~ConfigFortigate`
- HP: :class:`~ConfigHPCommware`
- Junos: :class:`~ConfigJunos`
"""
import re
from collections import namedtuple
from typing import List
from .core import ConfigLineList, ConfigLine
import pyparsing


def line_parse_checker(line):
    """
    Checks if the given line parses fully--ie, all quotes are closed
    """
    quote_stack = [None]

    prev_char = None
    for char in line:
        top_stack = quote_stack[-1]

        if char in ("'", '"') and prev_char != "\\":
            if char == top_stack:
                quote_stack.pop()
            else:
                quote_stack.append(char)

        prev_char = char

    return len(quote_stack) == 1


class ConfigBase(ConfigLineList):
    """
    Common configuration base operations

    :class:`~ConfigBase` is really just a specialized :class:`~.core.ConfigLineList`
    that can hold some settings and act like a :class:`~.core.ConfigLine`
    in terms of having a parent (`None`) and children.

    Refer to :class:`~.core.ConfigLineList` for filtering and searching options
    after you've parsed a configuration file.
    """

    #: Defaults to ! as the comment marker, following Cisco convention. If more
    # complex comment checking is needed override is_comment()
    comment_marker = "!"

    #: Default setting for `full_match` in `filter`. Defaults to True to prevent
    #: a search from also matching the "no" version of the line.
    full_match = True

    #: How far tree_display() should indent children. Has no effect on parsing
    indent_size = 2

    #: Original configuration lines, before any parsing occured. The
    #: :attr:`~ConfigLine.line_number` from a :class:`~ConfigLine` will match
    #: up with this list
    original_lines = None

    #: Exists to make walking up a parent tree easier--just look for parent=None to stop
    #:
    #: Contrived example:
    #:
    #: .. code:: python
    #:
    #:     current_line = config.filter("no shutdown", depth=None)
    #:     while current_line.parent is not None:
    #:         print(current_line)
    #:         current_line = current_line.parent
    parent = None

    def __init__(
        self,
        name="Network Config",
        original_lines: List[str] = None,
        comment_marker: str = "!",
        full_match_default: bool = True,
        indent_size_default: int = 2,
    ):
        """
        Configures settings used by :class:`~ConfigLine` methods

        In addition, subclasses should override this to parse the configuration file
        into :class:`~ConfigLine`s. See :class:`~ConfigIOS` for an example of this.
        """
        super().__init__()
        self.name = name
        self.comment_marker = comment_marker
        self.full_match = full_match_default
        self.original_lines = original_lines or []
        self.indent_size = indent_size_default

    @property
    def children(self) -> ConfigLineList:
        """
        Allow for use of ".children" for consistency with :class:`~ConfigLine`

        Returns `self`, which is already a :class:`~ConfigLineList`. It
        is likely cleaner to not use this. I.E.:

        .. code:: python

            config = ConfigIOS(running_config_contents)

            # Prefer this
            config.filter("interface .+")

            # Only use this if it looks clearer in context
            config.children.filter("interface .+")
        """
        return self


class ConfigIOS(ConfigBase):
    """
    Parses Cisco IOS-style configuration into common config format

    Supported command output:

    - `show running-config`
    - `show running-config all`
    - `show startup-config`

    See :class:`~ConfigBase` for more information.
    """

    def __init__(self, config_content):
        """
        Break all lines up into tree
        """
        super().__init__(
            name="IOS Config",
            original_lines=config_content.splitlines(),
            comment_marker="!",
        )

        parent_stack = {0: self}
        last_line = None
        last_indent = 0
        for lineno, line in enumerate(self.original_lines, start=1):
            if line.strip() == "--More--":
                continue

            # Determine our config depth and compare to the previous line's depth
            # The top-level config is always on the stack, so account for that
            matches = re.match(r"^(?P<spaces>\s*)", line)
            new_indent = len(matches.group("spaces"))

            if new_indent > last_indent:
                # Need to change parents to the last item of our current parent
                parent_stack[new_indent] = last_line

            curr_parent = parent_stack[new_indent]
            last_indent = new_indent
            last_line = ConfigLine(
                config_manager=self,
                parent=curr_parent,
                text=line.strip(),
                line_number=lineno,
            )
            curr_parent.children.append(last_line)


class ConfigNXOS(ConfigIOS):
    """
    Parses Cisco NX-OS-style configuration into common config format

    See :class:`~ConfigIOS` for more information.
    """


class ConfigASA(ConfigBase):
    """
    Parses Cisco ASA-style configuration into common config format

    Supported command output:

    - `show running-config`
    - `show running-config all`
    - `show startup-config`

    See :class:`~ConfigBase` for more information.
    """

    def __init__(self, config_content):
        """
        Break all lines up into tree
        """
        super().__init__(
            name="ASA Config",
            original_lines=config_content.splitlines(),
            comment_marker="!",
        )

        parent_stack = {0: self}
        last_line = None
        last_indent = 0
        for lineno, line in enumerate(self.original_lines, start=1):
            # ASAs are full of blank lines that don't matter
            if not line.strip():
                continue

            # Determine our config depth and compare to the previous line's depth
            # The top-level config is always on the stack, so account for that
            matches = re.match(r"^(?P<spaces>\s*)", line)
            new_indent = len(matches.group("spaces"))

            if new_indent > last_indent:
                # Need to change parents to the last item of our current parent
                parent_stack[new_indent] = last_line

            curr_parent = parent_stack[new_indent]
            last_indent = new_indent
            last_line = ConfigLine(
                config_manager=self,
                parent=curr_parent,
                text=line.strip(),
                line_number=lineno,
            )
            curr_parent.children.append(last_line)


class ConfigHPCommware(ConfigBase):
    """
    Parses HP Commware-style configuration into common config format

    See :class:`~ConfigBase` for more information.
    """

    def __init__(self, config_content):
        """
        Break all lines up into tree
        """
        super().__init__(
            name="HP Config",
            original_lines=config_content.splitlines(),
            comment_marker="#",
        )

        # lines = enumerate(self.original_lines, start=1)
        parent_stack = {0: self}
        last_line = None
        last_indent = 0
        for lineno, line in enumerate(self.original_lines, start=1):
            if not line.strip() or line.strip() == "--More--":
                continue

            # Determine our config depth and compare to the previous line's depth
            # The top-level config is always on the stack, so account for that
            matches = re.match(r"^(?P<spaces>\s*)", line)
            new_indent = len(matches.group("spaces"))

            if new_indent > last_indent:
                # Need to change parents to the last item of our current parent
                parent_stack[new_indent] = last_line

            curr_parent = parent_stack[new_indent]
            if curr_parent.is_comment():
                # HP indents the top level lines... sometimes. When there are
                # no children, I think. Reset that
                curr_parent = parent_stack[0]

            last_indent = new_indent
            last_line = ConfigLine(
                config_manager=self,
                parent=curr_parent,
                text=line.strip(),
                line_number=lineno,
            )
            curr_parent.children.append(last_line)


class ConfigJunos(ConfigBase):
    """
    Parses a Juniper OS (Junos)-style configuration into common config format

    Supported command outputs are:

    - `show configuration`
    - `save`

    See :class:`~ConfigBase` for more information.
    """

    def __init__(self, config_content):
        """
        Break all lines up into tree
        """
        super().__init__(
            name="Junos Config",
            original_lines=config_content.splitlines(),
            comment_marker="#",
        )

        parent_stack = [self]
        last_line = None
        for lineno, line in enumerate(self.original_lines, start=1):
            curr_parent = parent_stack[-1]

            command = True
            block_start = False
            block_end = False
            modified_line = line.strip()
            if modified_line.endswith(";"):
                command = True
            elif modified_line.endswith("{"):
                block_start = True
            elif modified_line.endswith("}"):
                block_end = True

            if block_start or block_end or command:
                modified_line = modified_line[:-1]

            if not block_end:
                last_line = ConfigLine(
                    config_manager=self,
                    parent=curr_parent,
                    text=modified_line.strip(),
                    line_number=lineno,
                )
                curr_parent.children.append(last_line)

            # Change indent?
            if block_start:
                parent_stack.append(last_line)
            elif block_end:
                parent_stack.pop()


class ConfigFortigate(ConfigBase):
    """
    Parses Fortinet-style configuration into common config format

    Supported command output:

    - `show system`

    See :class:`~ConfigBase` for more information.
    """

    def __init__(self, config_content):
        """
        Break all lines up into tree
        """
        super().__init__(
            name="Fortigate Config",
            original_lines=config_content.splitlines(),
            comment_marker="#",
        )

        lines = enumerate(self.original_lines, start=1)
        parent_stack = {0: self}
        last_line = None
        last_indent = 0
        for lineno, line in lines:
            if not line.strip() or line.strip() == "--More--":
                continue

            # Determine our config depth and compare to the previous line's depth
            # The top-level config is always on the stack, so account for that
            matches = re.match(r"^(?P<spaces>\s*)", line)
            new_indent = len(matches.group("spaces"))

            while not line_parse_checker(line):
                # Keep adding lines to this one until it parses
                _, added_line = next(lines)
                line += "\n" + added_line

            if new_indent > last_indent:
                # Need to change parents to the last item of our current parent
                parent_stack[new_indent] = last_line

            curr_parent = parent_stack[new_indent]
            last_indent = new_indent
            last_line = ConfigLine(
                config_manager=self,
                parent=curr_parent,
                text=line.strip(),
                line_number=lineno,
            )
            curr_parent.children.append(last_line)
