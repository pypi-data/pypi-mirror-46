# -*- coding: utf-8 -*-

import os

here = os.path.dirname(__file__)


def get_rst(filename):
    abspath = os.path.join(here, filename)
    with open(abspath, "rb") as f:
        rst = f.read().decode("utf-8")
    return rst


def edit_rst(rst):
    return "\n".join([
        line.rstrip()
        for line in rst.split("\n")
    ]).strip()


def compare_with(rst, filename):
    assert edit_rst(rst) == edit_rst(get_rst(filename))
