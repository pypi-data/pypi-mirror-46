"""Helpers for text translation"""

import gettext
import logging

from flask import request

# Global cache for installed gettext object for different locales
_gettext_cache = {}
logger = logging.getLogger(__name__)


def get_locale_from_request():
    """
    Gets locale settings from URL parameter
    or JSON body.
    """

    locale = request.args.get('locale')
    if locale:
        return locale

    if request.json:
        return request.json.get('locale', 'en_US')

    return 'en_US'


def get_translator(locale, domain, locale_dir='locales'):
    """
    Gets cached gettext function for translation.

    Args:
        locale (str): locale, e.g. en_US, zh_CN
        domain (str): domain of translation, which affect
            name of translation resources to be loaded
        locale_dir (str, optional): directory to locate
            translation message resources

    Returns:
        [type]: [description]
    """

    logger.info('Loading translator for locale %s from %s for domain %s',
                locale, locale_dir, domain)

    cache_key = locale + '/' + domain
    translation = _gettext_cache.get(cache_key)
    if not translation:
        lang = gettext.translation(domain,
                                   localedir=locale_dir,
                                   languages=[locale, 'en_US'])
        lang.install()
        translation = lang.gettext
        _gettext_cache[cache_key] = translation

    return translation


def translate_fields(fields, locale='en_US', locale_dir='locales', lc_domain='fields'):
    """
    Translates the given fields map for the given locale.

    Args:
        fields (list): Fields to translate.
        locale (str): Locale.
        locale_dir (str): Directory where to locate LC files.
        lc_domain (str): Domain name for LC files.
    """

    assert isinstance(fields, list)
    assert locale

    _ = get_translator(locale, lc_domain, locale_dir=locale_dir)

    for node in fields:
        name = node.get('name')
        if name:
            node['name'] = _(name)
        children = node.get('children')
        if children:
            translate_fields(children, locale, locale_dir, lc_domain)


def translate_json(json_obj, locale='en_US', locale_dir='locales', lc_domain='config'):
    """
    Recursively translate (in-place) string values in a json object
    for those quoted with _()

    Args:
        json_obj (json object): The json object.
        locale (str): Defaults to 'en_US'. Locale.
        locale_dir (str): Directory where to locale LC files.
        lc_domain (str): Domain name for LC files.
    """

    assert locale
    assert locale_dir
    assert lc_domain

    _ = get_translator(locale, lc_domain, locale_dir=locale_dir)

    def _trans(value):
        if value.startswith('_(') and value.endswith(')'):
            return _(value[2:-1])
        return value

    if isinstance(json_obj, dict):
        for key, value in json_obj.items():
            if isinstance(value, str):
                json_obj[key] = _trans(value)
            else:
                translate_json(value, locale=locale)
    elif isinstance(json_obj, list):
        for i, value in enumerate(json_obj):
            if isinstance(value, str):
                json_obj[i] = _trans(value)
            else:
                translate_json(value, locale=locale)
