.. contents:: Table of Contents


Introduction
============

This package is an addon for `ftw.simplelayout <http://github.com/4teamwork/ftw.simplelayout>`_. Please make sure you
already installed ``ftw.simplelayout`` on your plone site before installing this addon.

SliderBlock provides the integration of an image slider on a page powered
by ftw.simplelayout. It uses the existing functionality of ftw.slider.

Compatibility
-------------

Plone 4.3.x

.. image:: https://jenkins.4teamwork.ch/job/ftw.sliderblock-master-test-plone-4.3.x.cfg/badge/icon
   :target: https://jenkins.4teamwork.ch/job/ftw.sliderblock-master-test-plone-4.3.x.cfg


Installation
============

- Add the package to your buildout configuration:

::

    [instance]
    eggs +=
        ...
        ftw.sliderblock


Usage
=====

Drag a SliderBlock form the toolbox into your page and add some SliderPane
by switching to the folder listing view of the SliderBlock.


Development
===========

**Python:**

1. Fork this repo
2. Clone your fork
3. Shell: ``ln -s development.cfg buidlout.cfg``
4. Shell: ``python boostrap.py``
5. Shell: ``bin/buildout``

Run ``bin/test`` to test your changes.

Or start an instance by running ``bin/instance fg``.


Links
=====

- Github: https://github.com/4teamwork/ftw.sliderblock
- Issues: https://github.com/4teamwork/ftw.sliderblock/issues
- Pypi: http://pypi.python.org/pypi/ftw.sliderblock
- Continuous integration: https://jenkins.4teamwork.ch/search?q=ftw.sliderblock


Copyright
=========

This package is copyright by `4teamwork <http://www.4teamwork.ch/>`_.

``ftw.sliderblock`` is licensed under GNU General Public License, version 2.
