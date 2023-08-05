.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.

==============================================================================
jazkarta.tesserae
==============================================================================

This package contains a collection of extensions intended to be used with
``plone.app.mosaic`` on Plone 5+.


Features
--------

- Slider image content type used as the basis for a simple bootstrap image
  carousel.

- Slider view and configuration for folders containing slider images
  (though it will also work with other image containing content). A
  folder with this view applied will appear as a slider when used within
  mosaic's existing content tile.

- A full width tile style, which causes a tile to expand past the bounds
  of the grid width to the full window width.


Translations
------------

This product has been translated into

- English (U.S.)


Installation
------------

Install jazkarta.tesserae by adding it to your buildout::

    [buildout]

    ...

    eggs =
        jazkarta.tesserae


and then running ``bin/buildout``

On Plone 4.3 an additional version pin for plone.app.vocabularies is required:

    [versions]
    plone.app.vocabularies = 2.1.24


Contribute
----------

- Issue Tracker: https://github.com/jazkarta/jazkarta.tesserae/issues
- Source Code: https://github.com/jazkarta/jazkarta.tesserae


License
-------

The project is licensed under the GPLv2.
