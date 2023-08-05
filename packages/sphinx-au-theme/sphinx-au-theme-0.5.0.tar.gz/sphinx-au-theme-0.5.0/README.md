sphinx-au-theme
===============

This is a theme for Sphinx based on the design of the Aarhus University,
Denmark website. Specifically, the theme emulates a "department" page, but
with minor modifications:

* simplified header without search and menu buttons,
* simplified footer with only one column for contact information,
* the AU Passata font is used for body text, instead of Georgia.

All static assets (fonts, icons, logos) are included in the theme. The
available options are:

* sitename
* phone
* email

Development
-----------

Bump the version number in `setup.py`, then:

```
$ rm -rf dist/
$ python setup.py sdist bdist_wheel
$ twine upload dist/*
```
