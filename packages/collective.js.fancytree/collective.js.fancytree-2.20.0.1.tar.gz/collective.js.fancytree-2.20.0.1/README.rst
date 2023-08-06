=======================
collective.js.fancytree
=======================

Introduction
============

This addon register Fancytree to Plone resource registry.

version: 2.20.0

About Fancytree
===============

Fancytree (sequel of DynaTree 1.x) is a JavaScript dynamic tree view plugin for jQuery with support for persistence, keyboard, checkboxes, tables, drag'n'drop, and lazy loading.


Declare the package as a dependency
===================================

You will use this package as a dependency of your site or plugin package.

- in `setup.py`, add `collective.js.fancytree` in `install_requires` section,
- in `configure.zcml`, add `<include package="collective.js.fancytree" />`,
- in your `profiles/default/metadata.xml`, add:
    - `<dependency>profile-collective.js.fancytree:all</dependency>` to add fancytree with all plugins,
    - **or** `<dependency>profile-collective.js.fancytree:default</dependency>` to add basic fancytree,
    - **and** `<dependency>profile-collective.js.fancytree:theme-*****</dependency>` to add the theme.

Available themes: `theme-lion` and `theme-vista`.

Credits
=======

- Gauthier BASTIEN <gauthier.bastien@imio.be>
- Thomas DESVENAIN <thomas.desvenain@gmail.com>
- Fancytree: https://github.com/mar10/fancytree

