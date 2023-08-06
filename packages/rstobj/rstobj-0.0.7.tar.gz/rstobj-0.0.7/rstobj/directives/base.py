# -*- coding: utf-8 -*-

import attr
from ..base import RstObj


@attr.s
class Directive(RstObj):
    class_ = attr.ib(default=None)  # type: str
    name = attr.ib(default=None)    # type: str

    meta_directive_keyword = None   # type: str

    @property
    def arg(self):  # pragma: no cover
        raise NotImplementedError
