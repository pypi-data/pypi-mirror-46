"""Settings of cmsplugin_zinnia"""
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


HIDE_ENTRY_MENU = getattr(settings, 'CMSPLUGIN_ZINNIA_HIDE_ENTRY_MENU', True)

# Shipped plugin templates base which is added to custom ones in
# "PLUGINS_TEMPLATES"
BASE_PLUGINS_TEMPLATES = getattr(settings, 'CMSPLUGIN_ZINNIA_BASE_TEMPLATES', [
    ('cmsplugin_zinnia/entry_list.html', _('Entry list (default)')),
    ('cmsplugin_zinnia/entry_detail.html', _('Entry detailed')),
    ('cmsplugin_zinnia/entry_slider.html', _('Entry slider'))
])

# If not defined, will use the first item from available template list
DEFAULT_PLUGINS_TEMPLATES = getattr(settings,
                                    'CMSPLUGIN_ZINNIA_DEFAULT_TEMPLATE', None)

PLUGINS_TEMPLATES = getattr(settings, 'CMSPLUGIN_ZINNIA_TEMPLATES', [])

APP_URLS = getattr(settings, 'CMSPLUGIN_ZINNIA_APP_URLS', ['zinnia.urls'])

APP_MENUS = getattr(settings, 'CMSPLUGIN_ZINNIA_APP_MENUS',
                    ['cmsplugin_zinnia.menu.EntryMenu',
                     'cmsplugin_zinnia.menu.CategoryMenu',
                     'cmsplugin_zinnia.menu.TagMenu',
                     'cmsplugin_zinnia.menu.AuthorMenu'])
