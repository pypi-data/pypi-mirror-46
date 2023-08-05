.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.

===================
jazkarta.abtesttile
===================

This Plone addon provides a new Tile type for Mosaic Layout views.
It is a variation on a RichText tile which provides two WYSIWYG HTML
fields. It will randomly show one of the two HTML fields based on a
weighted ratio, for the purpose of A/B testing parts of a page layout.

Features
--------

- Includes optional support for custom JS to run with each rendered
  HTML option.

- Includes optional support for adding a campaign query string variable
  to any links in the rendered HTML, indicating whether option A or B
  was the source for analytics tracking.

- Provides a custom permision to restrict adding and editing of A/B
  Test Tiles to more privileged users.

Installation
------------

Install jazkarta.abtesttile by adding it to your buildout::

    [buildout]

    ...

    eggs =
        jazkarta.abtesttile


and then running ``bin/buildout``


Contribute
----------

- Issue Tracker: https://github.com/collective/jazkarta.abtesttile/issues
- Source Code: https://github.com/collective/jazkarta.abtesttile


Support
-------

If you are having issues, please let us know at info<at>jazkarta.com


License
-------

The project is licensed under the GPLv2.
