# -*- coding: utf-8 -*-

"""
Created on 2020-03-21
:author: Oshane Bailey (b4.oshany@gmail.com)
"""

pytest_plugins = "kotti"

from pytest import fixture


@fixture(scope='session')
def custom_settings():
    import kotti_audit.resources
    kotti_audit.resources  # make pyflakes happy
    return {
        'kotti.configurators': 'kotti_tinymce.kotti_configure '
                               'kotti_audit.kotti_configure'}
