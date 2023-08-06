.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.

==================================
collective.portlet.existingcontent
==================================

Allows to show data of an existing content object (Document) inside a portlet.


Features:
---------

- add & change "Existing Content" Portlet.
- relate to Document object.
- allow/disallow display of the Document title
- allow/disallow display of the Document description
- allow/disallow display of the Document text

Todo:
-----

- allow/disallow display of the Document leadimage
- control which content types are allowed


Translations
------------

This product has been translated into

- English
- German


Installation
------------

Install collective.portlet.existingcontent by adding it to your buildout::

    [buildout]

    ...

    eggs =
        collective.portlet.existingcontent


and then running ``bin/buildout``


Support & Contribute
--------------------

If you are having issues, please let us know.

- Issue Tracker: https://github.com/collective/collective.portlet.existingcontent/issues
- Source Code: https://github.com/collective/collective.portlet.existingcontent


License
-------

The project is licensed under the GPLv2.
