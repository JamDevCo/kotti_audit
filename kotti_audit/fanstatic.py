# -*- coding: utf-8 -*-

"""
Created on 2020-03-21
:author: Oshane Bailey (b4.oshany@gmail.com)
"""

from __future__ import absolute_import, division, print_function

from fanstatic import Group
from fanstatic import Library
from fanstatic import Resource
from kotti_bstable.fanstatic import css_and_js as bst_css_js


library = Library("kotti_audit", "static")

css_and_js = Group([
    Resource(
        library,
        "styles.css",
        minified="styles.min.css"),
    Resource(
        library,
        "scripts.js",
        minified="scripts.min.js", depends=[bst_css_js])
])
