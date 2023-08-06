# -*- coding: utf-8 -*-

import os
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader(os.path.dirname(__file__)))
