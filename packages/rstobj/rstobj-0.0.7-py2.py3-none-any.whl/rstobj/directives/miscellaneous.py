# -*- coding: utf-8 -*-

"""
Other directives.
"""

import attr
from .base import Directive


@attr.s
class Include(Directive):
    """
    ``.. include::`` directive. Include an external document fragment.

    Example::

        inc = Include(path="README.rst")
        inc.render()

    Output::

        .. include:: README.rst

    Parameters definition see here http://docutils.sourceforge.net/docs/ref/rst/directives.html#including-an-external-document-fragment.
    """
    path = attr.ib(default=None)    # type: str
    start_line = attr.ib(default=None)  # type: int
    end_line = attr.ib(default=None)  # type: int
    start_after = attr.ib(default=None)  # type: str
    end_before = attr.ib(default=None)  # type: str
    literal = attr.ib(default=None)  # type: bool
    code = attr.ib(default=None)  # type: str
    number_lines = attr.ib(default=None)  # type: int
    encoding = attr.ib(default=None)  # type: str
    tab_width = attr.ib(default=None)  # type: int

    meta_directive_keyword = "include"
    meta_not_none_fields = ("path",)

    @property
    def arg(self):
        return self.path
