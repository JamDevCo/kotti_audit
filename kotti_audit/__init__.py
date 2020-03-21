# -*- coding: utf-8 -*-

"""
Created on 2020-03-21
:author: Oshane Bailey (b4.oshany@gmail.com)
"""

from kotti.resources import File
from pyramid.i18n import TranslationStringFactory
from kotti.util import Link
from kotti_controlpanel import CONTROL_PANEL_LINKS as CPANEL_PAGE_LINKS

_ = TranslationStringFactory('kotti_audit')


def kotti_configure(settings):
    """ Add a line like this to you .ini file::

            kotti.configurators =
                kotti_audit.kotti_configure

        to enable the ``kotti_audit`` add-on.

    :param settings: Kotti configuration dictionary.
    :type settings: dict
    """

    settings['pyramid.includes'] += ' kotti_audit'
    settings['kotti.alembic_dirs'] += ' kotti_audit:alembic'
    CPANEL_PAGE_LINKS.append(
        Link('audit-log', title=_(u'Audit Log'))
    )

    if 'kotti_controlpanel.kotti_configure' not in settings['kotti.configurators']:
        settings['kotti.configurators'] += '\nkotti_controlpanel.kotti_configure'
        settings['kotti.base_includes'] += ' kotti_controlpanel'


def includeme(config):
    """ Don't add this to your ``pyramid_includes``, but add the
    ``kotti_configure`` above to your ``kotti.configurators`` instead.

    :param config: Pyramid configurator object.
    :type config: :class:`pyramid.config.Configurator`
    """

    config.add_translation_dirs('kotti_audit:locale')
    config.add_static_view('static-kotti_audit', 'kotti_audit:static')

    config.scan(__name__)
