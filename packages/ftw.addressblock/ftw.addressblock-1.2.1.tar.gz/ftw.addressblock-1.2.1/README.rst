ftw.addressblock
################

This package is an addon for `ftw.simplelayout <http://github.com/4teamwork/ftw.simplelayout>`_. Please make sure you
already installed ``ftw.simplelayout`` on your plone site before installing this addon.

This add-on installs a new content type which can be used to display address data.

Extras
======

There is an extra ``geo`` which installs optional geo and map support. If you
want to use this feature you must install both the ``default`` and the ``geo``
profile in your policy (the  ``geo`` profile won't install the  ``default``
profile).

Since ``1.2.1`` the zoomlevel and maplayer defined in the addressblocks edit panel
is saved. However, this will only work together with ``ftw.simplelayout`` versions
``2.1.0`` and ``1.23.10`` (backport) or higher. For more information see
`ftw.simplelayout#530 <https://github.com/4teamwork/ftw.simplelayout/pull/530>`_
and `ftw.addressblock#25 <https://github.com/4teamwork/ftw.addressblock/pull/25>`_.

There is an extra ``contact`` which will provide a contact form. If you
want to use this feature you must install both the ``default`` and the ``contact``
profile in your policy (the  ``contact`` profile won't install the  ``default``
profile).

The contact form provides a ReCaptcha field which is only rendered for anonymous
users.



Development
===========

**Python:**

1. Fork this repo
2. Clone your fork
3. Shell: ``ln -s development.cfg buildout.cfg``
4. Shell: ``python boostrap.py``
5. Shell: ``bin/buildout``

Run ``bin/test`` to test your changes.

Or start an instance by running ``bin/instance fg``.


Links
=====

- GitHub: https://github.com/4teamwork/ftw.addressblock
- Issues: https://github.com/4teamwork/ftw.addressblock/issues
- PyPI: http://pypi.python.org/pypi/ftw.addressblock
- Continuous integration: https://jenkins.4teamwork.ch/search?q=ftw.addressblock


Copyright
=========

This package is copyright by `4teamwork <http://www.4teamwork.ch/>`_.

``ftw.addressblock`` is licensed under GNU General Public License, version 2.
