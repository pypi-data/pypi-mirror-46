# -*- coding: utf-8 -*-

"""
Bullet list.
"""

import attr
from ..base import RstObj


@attr.s
class BulletList(RstObj):
    """
    Bullet list class.

    Example::

        blist = BulletList(items=["a", "b", "c"])
        blist.render()

    Output::

        - a
        - b
        - c

    More example: http://docutils.sourceforge.net/docs/user/rst/quickref.html#bullet-lists
    """
    items = attr.ib()   # type: list
