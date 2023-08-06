# -*- coding: utf-8 -*-

"""
Enumerate list.
"""

import attr
from ..base import RstObj


@attr.s
class EnumList(RstObj):
    """
    Enumerate list class.

    Example::

        blist = Enumerate(items=["a", "b", "c"], start_num=3)
        blist.render()

    Output::

        3. a
        4. b
        5. c

    More example: http://docutils.sourceforge.net/docs/user/rst/quickref.html#enumerated-lists
    """
    items = attr.ib()   # type: list
    start_num = attr.ib(default=1)  # type: int
