==============================================================================
collective.tiles.advancedstatic
==============================================================================

A tile that shows html text, allowing to add some defined styles, class and other option

Features
--------

- Emulates the old text portlet with some extra fields
- Customizable footer label
- Customizable "read more" link
- Customizable header background image
- Customizable additional css classes
- Select a Preset style from list
- Mosaic-ready


Installation
------------

Install collective.tiles.advancedstatic by adding it to your buildout::

    [buildout]
    ...
    eggs =
        collective.tiles.advancedstatic


and then running ``bin/buildout``


Usage
-----

You can't use this tile without a tile manager (or maybe, you can if you create
new tiles manually in some specific context) like `Mosaic <https://pypi.python.org/pypi/plone.app.mosaic>`_ or `redturtle.tiles.management <https://github.com/RedTurtle/redturtle.tiles.management>`_


Preset styles
-------------

If you need to give users the
This is just select with a list of css classes with user-friendly names that will be appended to the tile container.

To populate this list, you need to set a series of values in a registry entry: `Advanced static tiles: available CSS styles`
Each value is a string with css class name and human-friendly name separated by a "|" character, like this::

    tile-red|tile with red background
    tile-blue-no-title|tile with blue background without title

where tile-red and tile-blue-no-title are css classes with some specific css rules in the theme.


Translations
------------

This product has been translated into

- Italian


Contribute
----------

- Issue Tracker: https://github.com/collective/collective.tiles.advancedstatic/issues
- Source Code: https://github.com/collective/collective.tiles.advancedstatic

Credits
-------

Developed with the support of:

* `Regione Emilia-Romagna`__

Regione Emilia-Romagna supports the `PloneGov initiative`__.

__ http://www.regione.emilia-romagna.it/
__ http://www.plonegov.it/

Authors
-------

This product was developed by RedTurtle Technology team.

.. image:: http://www.redturtle.it/redturtle_banner.png
   :alt: RedTurtle Technology Site
   :target: http://www.redturtle.it/

License
-------

The project is licensed under the GPLv2.
