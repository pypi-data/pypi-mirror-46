# -*- coding: utf-8 -*-

"""

This module is a sphinx-doc add-on to implement the following markup::

    .. icontable:: <dirname>
        :n_columns: <n_columns>

For example::

    .. icontable:: demo-images
        :n_columns: 3

It looks for image file in <currend_dir>/<dirname>, and put them into a rst
list table, <n_columns> item each row.
"""

from __future__ import unicode_literals
import sphinx.util
from docutils import nodes
from docutils.parsers.rst import Directive
from docutils.statemachine import StringList
from pathlib_mate import Path
from rstobj.directives import ListTable, Image

try:  # in python2
    from itertools import izip_longest as zip_longest
except:  # in python3
    from itertools import zip_longest


def grouper(iterable, n, fillvalue=None):
    """
    Collect data into fixed-length chunks or blocks.

    Example::

        >>> list(grouper(range(10), n=3, fillvalue=None))
        [(0, 1, 2), (3, 4, 5), (6, 7, 8), (9, None, None)]

    **中文文档**

    将一个序列按照尺寸n, 依次打包输出, 如果元素不够n的包, 则用 ``fillvalue`` 中的值填充。
    """
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


def derive_rst(current_dir, image_dir, n_columns):
    """
    scan ``image_dir`` find all image path, find the relative path to ``current_dir``,
    and put them in a table, ``n_columns`` width. return the list table rst
    directive text.
    """
    current_dir, image_dir = Path(current_dir), Path(image_dir)
    image_list = [
        Image(uri=str(p.relative_to(current_dir)), height=64, width=64)
        for p in image_dir.select_image()
    ]
    data = list(grouper(image_list, n_columns))
    ltable = ListTable(
        data=data, header=False, index=False
    )
    return ltable.render()


class IconTable(Directive):
    """
    ``.. icontable:: <dirpath>`` markup implementation.
    """
    required_arguments = 1

    option_spec = {
        "n_columns": int
    }

    def run(self):
        node = nodes.Element()
        node.document = self.state.document
        current_file = self.state.document.current_source
        current_dir = Path(current_file).parent
        image_dir = Path(Path(current_file).parent, self.arguments[0])
        n_columns = self.options.get("n_columns", 3)
        if image_dir.exists():
            output_rst = derive_rst(
                current_dir=current_dir, image_dir=image_dir,
                n_columns=n_columns,
            )
        else:
            output_rst = ""
        view_list = StringList(output_rst.splitlines(), source='')
        sphinx.util.nested_parse_with_titles(self.state, view_list, node)
        return node.children


def setup(app):
    app.add_directive("icontable", IconTable)


if __name__ == "__main__":
    rst = derive_rst(
        current_dir="/Users/sanhehu/Documents/GitHub/rstobj-project/docs/source",
        image_dir="/Users/sanhehu/Documents/GitHub/rstobj-project/docs/source/demo-images",
        n_columns=3,
    )
    print(rst)
