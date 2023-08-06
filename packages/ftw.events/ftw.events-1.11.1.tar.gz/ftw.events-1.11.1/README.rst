==============================================================================
ftw.events
==============================================================================

.. contents:: Table of Contents

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


Mopage Support
==============

``ftw.events`` provides integration for the mopage mobile app
(http://web.anthrazit.org/).


Data Endpoint
-------------

The view ``mopage.events.xml`` returns an XML-feed with the latest events within
the context it is called. It can becalled on any type of object.

- The mopage-API expects a ``partnerid`` and a ``importid``.
  They are incldued when submitted via GET-parameter, e.g.:
  ``http://foo.com/events/mopage.events.xml?partnerid=123&importid=456``

- The endpoint returns only 100 events by default.
  This can be changed with the parameter ``?per_page=200``.

- The endpoint returns ``Link``-headers in the response with pagination links.


Trigger behavior
----------------

The behavior ``ftw.events.behaviors.mopage.IPublisherMopageTrigger`` can be added
on a event folder in order to configure automatic notification to the mopage API
that new events are published.

In order for the behavior to work properly you need an ``ftw.publisher`` setup.
Only the receiver-side (public website) will trigger the notification.
A configured ``collective.taskqueue`` is required for this to work.

Buildout example:

.. code:: ini

    [instance]
    eggs +=
        ftw.events[mopage_publisher_receiver]

    zope-conf-additional +=
        %import collective.taskqueue
        <taskqueue />
        <taskqueue-server />


Then enable the behavior for the event folder type and configure the trigger
with the newly availabe fields.


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
