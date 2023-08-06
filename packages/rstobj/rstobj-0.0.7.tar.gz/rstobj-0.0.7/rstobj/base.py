# -*- coding: utf-8 -*-

"""
RestructuredText Object abstraction.
"""

import six
import attr
from attrs_mate import AttrsClass
from .templates import env
from .option import Options


@attr.s
class RstObj(AttrsClass):
    """
    The base restructured text object.
    """
    meta_not_none_fields = tuple()

    def validate_not_none_fields(self):
        for field in self.meta_not_none_fields:
            if getattr(self, field) is None:
                msg = "`{}.{}` can't be None!" \
                    .format(self.__class__.__name__, field)
                raise ValueError(msg)

    def __attrs_post_init__(self):
        self.validate_not_none_fields()

    @property
    def template_name(self):
        """
        Find template file.

        :rtype: str
        """
        return "{}.{}.rst".format(self.__module__, self.__class__.__name__)

    @property
    def template(self):
        """
        Return ``jinja2.Template`` instance.

        :rtype: str
        """
        return env.get_template(self.template_name)

    def render(self, indent=None, first_line_indent=None, **kwargs):
        """
        Render this object into text.

        :type indent: int
        :param indent: global indent. Indent length can be changed in
            :attr:`rstobj.option.Options.tab`.

        :type first_line_indent: int
        :param first_line_indent: sometimes we only need to indent
            first line, this option will overwrite the ``indent`` argument.

        :param kwargs: other optional arguments.

        :rtype: str
        """
        out = self.template.render(obj=self)
        if indent:
            origin_lines = out.split("\n")
            target_lines = [Options.tab * indent + line.rstrip()
                            for line in origin_lines]
            if first_line_indent is not None:
                if first_line_indent >= 0:
                    target_lines[0] = Options.tab * \
                        first_line_indent + origin_lines[0].rstrip()
                else:  # pragma: no cover
                    raise TypeError
            out = "\n".join(target_lines)
        return out

    @staticmethod
    def str_or_render(value, **kwargs):
        """
        If it is a string type, then just return. If it is a RstObj type,
        then return the rendered string.

        :rtype: str
        """
        if isinstance(value, RstObj):
            return value.render(**kwargs)
        else:
            return six.text_type(value)
