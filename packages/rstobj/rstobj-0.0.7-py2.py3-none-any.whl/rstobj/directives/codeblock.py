# -*- coding: utf-8 -*-

"""
code block related directives.
"""

import attr
from .base import Directive
from ..base import RstObj


@attr.s
class Code(RstObj):
    """
    Pure text code Snippet.
    """
    text = attr.ib(default=None)  # type: str

    meta_not_none_fields = ("text",)


@attr.s
class CodeBlockEmpty(Directive):
    """
    Example::

        code = "your code ..."
        cb = CodeBlockEmpty.from_string(code)
        cb.render()

    Output::

        ::

            your code ...
    """
    code = attr.ib(
        default=None,
        validator=attr.validators.instance_of(Code)
    )  # type: Code

    meta_not_none_fields = ("code",)

    @classmethod
    def from_string(cls, text):
        """
        Construct CodeBlock from string.

        :type text: str
        """
        return cls(code=Code(text=text))


@attr.s
class CodeBlockBase(CodeBlockEmpty):
    """
    Base class for language specified code block.
    """

    meta_lang = ""  # type: str

    class LangOptions(object):
        empty = ""
        python = "python"
        ruby = "ruby"
        r = "r"
        perl = "perl"
        c = "c"
        cpp = "cpp"
        html = "html"
        css = "css"
        javascript = "javascript"
        sql = "sql"
        scala = "scala"
        make = "make"
        bash = "bash"

    @property
    def template_name(self):
        return "{}.{}.rst".format(self.__module__, "CodeBlockBase")


code_block_doc_string = """
:param code: :class:`Code`.

Example::

    code = "your code ..."
    cb = CodeBlockLanguageName.from_string(code)
    cb.render()

Output::

    .. code-block: {}

        your code ...
""".strip()


@attr.s
class CodeBlock(CodeBlockBase):
    meta_lang = CodeBlockBase.LangOptions.empty
    __doc__ = code_block_doc_string.format(meta_lang)


@attr.s
class CodeBlockPython(CodeBlockBase):
    meta_lang = CodeBlockBase.LangOptions.python
    __doc__ = code_block_doc_string.format(meta_lang)


@attr.s
class CodeBlockRuby(CodeBlockBase):
    meta_lang = CodeBlockBase.LangOptions.ruby
    __doc__ = code_block_doc_string.format(meta_lang)


@attr.s
class CodeBlockR(CodeBlockBase):
    meta_lang = CodeBlockBase.LangOptions.r
    __doc__ = code_block_doc_string.format(meta_lang)


@attr.s
class CodeBlockPerl(CodeBlockBase):
    meta_lang = CodeBlockBase.LangOptions.perl
    __doc__ = code_block_doc_string.format(meta_lang)


@attr.s
class CodeBlockC(CodeBlockBase):
    meta_lang = CodeBlockBase.LangOptions.c
    __doc__ = code_block_doc_string.format(meta_lang)


@attr.s
class CodeBlockCPP(CodeBlockBase):
    meta_lang = CodeBlockBase.LangOptions.cpp
    __doc__ = code_block_doc_string.format(meta_lang)


@attr.s
class CodeBlockHTML(CodeBlockBase):
    meta_lang = CodeBlockBase.LangOptions.html
    __doc__ = code_block_doc_string.format(meta_lang)


@attr.s
class CodeBlockCSS(CodeBlockBase):
    meta_lang = CodeBlockBase.LangOptions.css
    __doc__ = code_block_doc_string.format(meta_lang)


@attr.s
class CodeBlockJavaScript(CodeBlockBase):
    meta_lang = CodeBlockBase.LangOptions.javascript
    __doc__ = code_block_doc_string.format(meta_lang)


@attr.s
class CodeBlockSQL(CodeBlockBase):
    meta_lang = CodeBlockBase.LangOptions.sql
    __doc__ = code_block_doc_string.format(meta_lang)


@attr.s
class CodeBlockScala(CodeBlockBase):
    meta_lang = CodeBlockBase.LangOptions.scala
    __doc__ = code_block_doc_string.format(meta_lang)


@attr.s
class CodeBlockMake(CodeBlockBase):
    meta_lang = CodeBlockBase.LangOptions.make
    __doc__ = code_block_doc_string.format(meta_lang)


@attr.s
class CodeBlockBash(CodeBlockBase):
    meta_lang = CodeBlockBase.LangOptions.bash
    __doc__ = code_block_doc_string.format(meta_lang)
