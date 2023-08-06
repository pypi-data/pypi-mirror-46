Changelog
=========

0.5.1
-----

* `#58`_: Fix Python 3 install issues related to unicode strings. Thanks to
  Zowie for inspiring the patch.

.. _#58: https://github.com/gregmuellegger/django-mobile/pull/58

0.5.0
-----

* Support for Django 1.7 and Django 1.8. Thanks to Jose Ignacio Galarza and to
  Anton Shurashov for the patches.

0.4.0
-----

* Python 3.3 compatibility, thanks Mirko Rossini for the patch.
* Dropping Django 1.3 and 1.4 support.

0.3.0
-----

* Dropping support for python 2.5 (it might still work but we won't test
  against it anymore).
* Fixing threading problems because of wrong usage of ``threading.local``.
  Thanks to Mike Shultz for the patch.
* Adding a cached template loader. Thanks to Saverio for the patch.

0.2.4
-----

* FIX: Cookie backend actually never really worked. Thanks to demidov91 for
  the report. 

0.2.3
-----

* FIX: set *flavour* in all cases, not only if a mobile browser is detected.
  Thanks to John P. Kiffmeyer for the report.

0.2.2
-----

* FIX: Opera Mobile on Android was categorized as mobile browser. Thanks to
  dgerzo for the report.
* Sniffing for iPad so that it doesn't get recognized as small mobile device.
  Thanks to Ryan Showalter for the patch.

0.2.1
-----

* Fixed packing issues that didn't include the django_mobile2.cache package.
  Thanks to *Scott Turnbull* for the report.

0.2.0
-----

* Restructured project layout to remove settings.py and manage.py from
  top-level directory. This resolves module-name conflicts when installing
  with pip's -e option. Thanks to *bendavis78* for the report.

* Added a ``cache_page`` decorator that emulates django's ``cache_page`` but
  takes flavours into account. The caching system would otherwise cache the
  flavour that is currently active when a cache miss occurs. Thanks to
  *itmustbejj* for the report.

* Added a ``CacheFlavourMiddleware`` that makes django's caching middlewares
  aware of flavours. We use interally the ``Vary`` response header and the
  ``X-Flavour`` request header.

0.1.4
-----

* Fixed issue in template loader that only implemented
  ``load_template_source`` but no ``load_template``. Thanks to tylanpince,
  rwilcox and Frédéric Roland for the report.

0.1.3
-----

* Fixed issue with ``runserver`` command that didn't handled all request
  independed from each other. Thanks to bclermont and Frédéric Roland for the
  report.

0.1.2
-----

* Fixed unreferenced variable error in ``SetFlavourMiddleware``.

0.1.1
-----

* Fixed ``is_usable`` attribute for ``django_mobile2.loader.Loader``. Thanks Michela Ledwidge for the report.

0.1.0
-----

* Initial release.
