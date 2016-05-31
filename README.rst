==============================================================================
ftw.events
==============================================================================

``ftw.events`` is a Plone add-on allowing you to add containers (event folders)
containing items representing an event (event page). It is backed by
``plone.app.event`` and is powered by ``ftw.simplelayout``.

This Plone add-on is compatible with Plone 4.3.x


Installation
************

- Add the package to your buildout configuration:

::

    [instance]
    eggs +=
        ...
        ftw.events

- Install the "default" GenericSetup profile.


Usage
*****

Start by creating a container which will hold the events by adding a *event folder*.
Add as many *event pages* to the event folder as you like.


Background
**********

The name of the content type *event page* has been chosen in order to avoid confusion
with the content type *event* of Plone.


Development
***********

**Python:**

1. Fork this repo
2. Clone your fork
3. Shell: ``ln -s development.cfg buildout.cfg``
4. Shell: ``python boostrap.py``
5. Shell: ``bin/buildout``

Run ``bin/test`` to test your changes.

Or start an instance by running ``bin/instance fg``.


Links
*****

- Github: https://github.com/4teamwork/ftw.events
- Issues: https://github.com/4teamwork/ftw.events/issues
- PyPI: http://pypi.python.org/pypi/ftw.events
- Continuous integration: https://jenkins.4teamwork.ch/search?q=ftw.events


Copyright
*********

This package is copyright by `4teamwork <http://www.4teamwork.ch/>`_.

``ftw.events`` is licensed under GNU General Public License, version 2.
