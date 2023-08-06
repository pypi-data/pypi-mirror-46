# -*- coding: utf-8 -*-

"""
Header markups.

Default `section header line <http://docutils.sourceforge.net/docs/user/rst/quickstart.html#sections>`_ character:

- header 1: ``=``
- header 2: ``-``
- header 3: ``~``
- header 4: ``+``
- header 5: ``*``
- header 6: ``#``
- header 7: ``^``
"""

import attr
from ..base import RstObj

dash_char_list = " _~"
ignore_char_list = """`*()[]{}<>"'"""


def to_label(title):
    """
    slugify title and convert to reference label.

    :rtype: str
    """
    for char in dash_char_list:
        title = title.replace(char, "-")
    for char in ignore_char_list:
        title = title.replace(char, "")
    return "-".join([
        chunk.strip() for chunk in title.split("-") if chunk.strip()
    ])


HEADER_CHAR_MAPPER = {
    1: "=",
    2: "-",
    3: "~",
    4: "+",
    5: "*",
    6: "#",
    7: "^",
}


@attr.s
class Header(RstObj):
    """
    A `Section Header <http://docutils.sourceforge.net/docs/user/rst/quickstart.html#sections>`_ markup.

    :param title: str, title text
    :param header_level: int, 1 ~ 7
    :param ref_label: str, cross domain reference label string. a global key
        for this header.
    :param auto_label: bool, if True, automatically slugify the title and use
        it as the reference label.

    Example::

        h = Header(title="Hello World", header_level=1, auto_label=True)
        h.render()

    Output::

        .. _hello-world:

        Hello World
        ===========
    """
    title = attr.ib()  # type: str
    header_level = attr.ib(default=None)  # type: int
    ref_label = attr.ib(default=None)  # type: str
    auto_label = attr.ib(default=False)  # type: bool

    _header_level = 0
    _bar_length = None

    meta_not_none_fields = ("header_level",)

    @header_level.validator
    def header_level_validator(self, attribute, value):
        if value is not None:
            if not (1 <= value <= 7):
                raise ValueError("header_level has to be between 1 - 7!")

    def __attrs_post_init__(self):
        super(Header, self).__attrs_post_init__()
        if self.auto_label and (self.ref_label is None):
            self.ref_label = to_label(self.title)

    @property
    def header_char(self):
        """
        :rtype: str
        """
        if self.header_level:
            return HEADER_CHAR_MAPPER[self.header_level]
        else:
            return HEADER_CHAR_MAPPER[self._header_level]

    @property
    def template_name(self):
        """
        :rtype: str
        """
        return "{}.{}.rst".format(self.__module__, "Header")

    def render(self, bar_length=None, **kwargs):
        if bar_length is None:
            self._bar_length = len(self.title)
        else:
            self._bar_length = bar_length
        return super(Header, self).render(**kwargs)


@attr.s
class HeaderLevel(Header):
    meta_not_none_fields = tuple()


header_doc_string = \
    """
Example::

    Header{level}
    {bar}
"""


def _build_doc_string(header_level):
    return header_doc_string.format(
        level=header_level,
        bar=HEADER_CHAR_MAPPER[header_level] * 7,
    )


@attr.s
class Header1(HeaderLevel):
    __doc__ = _build_doc_string(1)
    _header_level = 1


@attr.s
class Header2(HeaderLevel):
    __doc__ = _build_doc_string(2)
    _header_level = 2


@attr.s
class Header3(HeaderLevel):
    __doc__ = _build_doc_string(3)
    _header_level = 3


@attr.s
class Header4(HeaderLevel):
    __doc__ = _build_doc_string(4)
    _header_level = 4


@attr.s
class Header5(HeaderLevel):
    __doc__ = _build_doc_string(5)
    _header_level = 5


@attr.s
class Header6(HeaderLevel):
    __doc__ = _build_doc_string(6)
    _header_level = 6


@attr.s
class Header7(HeaderLevel):
    __doc__ = _build_doc_string(7)
    _header_level = 7
