"""
Choices helper are usable from migrations to avoid to trigger new migration
when settings choices are changed
"""
from cmsplugin_zinnia.settings import (BASE_PLUGINS_TEMPLATES,
                                       PLUGINS_TEMPLATES,
                                       DEFAULT_PLUGINS_TEMPLATES)


def get_template_choices():
    """
    Return list of all available template (shipped ones + custom)
    """
    return BASE_PLUGINS_TEMPLATES + PLUGINS_TEMPLATES


def get_default_template():
    """
    Return either a defined one from OO setting or the first of list returned
    by "get_template_choices"
    """
    return DEFAULT_PLUGINS_TEMPLATES or get_template_choices()[0][0]
