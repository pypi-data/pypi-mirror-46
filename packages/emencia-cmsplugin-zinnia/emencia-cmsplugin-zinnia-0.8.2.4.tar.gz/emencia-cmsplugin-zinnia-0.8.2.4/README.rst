========================
emencia-cmsplugin-zinnia
========================

Cmsplugin-zinnia is a bridge between `django-blog-zinnia`_ and
`django-cms`_.

This package provides plugins, menus and apphook to integrate your Zinnia
powered Weblog into your django-cms Web site.

The code bundled in this application is a copy of the original
``zinnia.plugins`` module, made for forward compatibility with
django-blog-zinnia > 0.11.


.. Note::
    This is a fork of original
    `cmsplugin-zinnia <https://github.com/django-blog-zinnia/cmsplugin-zinnia>`_
    to be able to release an alternative package to fix compatibility issues
    with ``DjangoCMS>=3.4``.

.. contents::

.. _installation:

Installation
============

Once Zinnia and the CMS are installed, you simply have to register
``cmsplugin_zinnia``, in the ``INSTALLED_APPS`` section of your
project's settings.

.. _entry-placeholder:

Entries with plugins
====================

If you want to use the plugin system of django-cms in your entries, an
extended ``Entry`` with a ``PlaceholderField`` is provided in this package.

Just add this line in your project's settings to use it. ::

  ZINNIA_ENTRY_BASE_MODEL = 'cmsplugin_zinnia.placeholder.EntryPlaceholder'

.. note::
   You have to keep in mind that the default migrations bundled with Zinnia
   do not reflect the addition made by the ``EntryPlaceholder`` model.

   A solution to initialize correctly the database can be: ::

     $ python manage.py makemigrations
     $ python manage.py migrate

Tips for using the apphook
==========================

If you want to use the apphook to provide the blog functionnalities under a
specific URL handled by the CMS, remember this tip:

* Once the apphook is registered, you can remove the inclusion of
  ``'zinnia.urls'`` in ``urls.py`` and then restart the server to see it in
  full effect.

.. _settings:

Settings
========

CMSPLUGIN_ZINNIA_APP_URLS
-------------------------
**Default value:** ``['zinnia.urls']``

The URLsets used for by the Zinnia AppHook.

CMSPLUGIN_ZINNIA_APP_MENUS
--------------------------
**Default value:** ::

  ['cmsplugin_zinnia.menu.EntryMenu',
   'cmsplugin_zinnia.menu.CategoryMenu',
   'cmsplugin_zinnia.menu.TagMenu',
   'cmsplugin_zinnia.menu.AuthorMenu']

List of strings representing the path to the `Menu` class provided by the
Zinnia AppHook.

CMSPLUGIN_ZINNIA_HIDE_ENTRY_MENU
--------------------------------
**Default value:** ``True``

Boolean used for displaying or not the entries in the ``EntryMenu`` object.

CMSPLUGIN_ZINNIA_TEMPLATES
--------------------------
**Default value:** ``[]`` (Empty list)

List of tuple for extending the plugins rendering templates.

Example: ::

  CMSPLUGIN_ZINNIA_TEMPLATES = [
    ('entry_custom.html', 'Entry custom'),
    ('entry_custom_bis.html', 'Entry custom bis')
    ]

CMSPLUGIN_ZINNIA_BASE_TEMPLATES
-------------------------------
**Default value:** ::

  [('cmsplugin_zinnia/entry_list.html', _('Entry list (default)')),
   ('cmsplugin_zinnia/entry_detail.html', _('Entry detailed')),
   ('cmsplugin_zinnia/entry_slider.html', _('Entry slider'))]

Available base templates, these are the shipped template from this application.
Commonly you will prefer to use ``CMSPLUGIN_ZINNIA_TEMPLATES`` to add new
templates.

CMSPLUGIN_ZINNIA_DEFAULT_TEMPLATE
---------------------------------
**Default value:** ``None``

Initial value for ``template_to_render`` field. If empty or undefined, initial
value will be the first item of available template choices.

.. _changelog:

Changelog
=========

0.8.2.4
-------

Fixed compatibility with ``Django>=2.0``. Validated as working with
``Django==2.1.8``, ``django-cms==3.6.0`` and ``django-blog-zinnia==0.20``.

0.8.2.3
-------

Fixed ``template_to_render`` field missing a default value that could result
to broken page when no template was selected at plugin creation.

* Past migrations have been modified to clean them from any hardcoded
  choices that triggered warning message about changed model needing new
  migration when you added new template choices;
* Added data migration to fix plugins entries with empty value for
  ``template_to_render`` fields, they will be filled with defaut template;
* ``template_to_render`` fields can no longer be empty, select input do not
  show anymore option for empty value;

Everything is backward compatible. After updating you will just need to
perform migration for ``cmsplugin_zinnia`` app.

0.8.2.2
-------

Fixed ``CMSLatestEntriesPlugin`` and ``CMSSelectedEntriesPlugin`` to use
selected template to render instead of default plugin one.

0.8.2.1
-------

Renamed ``cms_toolbar.py`` to ``cms_toolbars.py`` so Zinnia application appear again in CMS toolbar.

0.8.2
-----

Fixed compatibility with ``DjangoCMS>=3.4``:

* Merged `pull request #64 <https://github.com/django-blog-zinnia/cmsplugin-zinnia/pull/64>`_;
* Merged `pull request #65 <https://github.com/django-blog-zinnia/cmsplugin-zinnia/pull/65>`_;

0.8.1
-----

- Remove warnings with Django 1.9

0.8
---

- Compatibility with Django 1.8

0.7
---

- PlaceholderEntry mixin
- Compatibility with Django 1.7 and Zinnia 0.15

0.6
---

- Compatibility with Django-CMS 3.0

0.5.1
-----

- Python 3 compatibility fix
- Better help texts and legends

0.5
---

- Archives plugin
- Tag cloud plugin
- Author list plugin
- Categories plugins
- Featured entries filter
- Offset for latest entries
- Documentation improvements
- Configurable apphook's urls
- Support custom auth.User model
- Fix translations of the plugins
- Fix HTML rendering without context
- Compatibility with Django v1.5
- Compatibility with Zinnia v0.13
- Updating the buildout installation

0.4.1
-----

- Compatibility fix for Django-CMS 2.2+

0.4
---

- Fix issues with Entry.content rendering.
- Compatibility with latest version of Zinnia.

0.3
---

- Calendar plugin.
- QueryEntries plugin.
- Slider template for plugins.
- Documentation improvements.
- Fix breadcrumbs with month abbrev.
- Compatibility with Django 1.4 and Django-CMS 2.3.

0.2
---

- Better demo.
- Renaming modules.
- Fix dependancies with mptt.
- Fix ``EntryPlaceholder``'s Meta.
- ``0`` means all the entries on plugins.
- Set menu Nodes to invisible instead of removing.

0.1
---

- Initial release based on ``zinnia.plugins``.


.. _django-blog-zinnia: http://django-blog-zinnia.com/
.. _django-cms: http://django-cms.com/
