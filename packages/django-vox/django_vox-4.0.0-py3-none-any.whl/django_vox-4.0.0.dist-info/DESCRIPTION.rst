==========
Django Vox
==========

|pipeline-badge| |coverage-badge| |docs-badge| |pypi-badge|

Django vox is a django app that allow you to create and issue
different types of notifications. Notifications can have different
kinds of parameters which allow for convenient editing in the admin.

Features
---------------

* Add and edit notifications from the admin
* Built-in message editor provides drop-down of available template variables
  and supports previewing
* Supports many backends: email (html & text), SMS (Twilio), Twitter, Slack,
  Postmark, XMPP, JSON webhooks, and Activity Streams
* Supports attachments
* Built in site contacts that can be used to send emails to admins, or update
  your organization‘s Twitter account, or send out webhooks
* Flexible API allows you to define your own user preferences about which user
  gets which kind of notification
* Set custom “from” addresses
* Send messages in bulk (all together) or individually customized messages


Why this exists
---------------

TLDR: Because I am lazy and I don't want to spend my evening doing
a deploy just because marketing wants to update the text in their
latest spam mail.

In a few more words:

* Editing copy for notifications shouldn't have to be done by programmers.
  This means:

  1. The notification templates should be editable in the admin
  2. The information necessary to correctly make a template, whether
     it's a template ID or parameters) should be available in the admin
     page. It shouldn't be necessary to look through source code just to
     make a notification work.
  3. Number 2 is actually a fairly difficult problem.

* People have different ways of interacting with computers, and one
  way of doing notifications (i.e. email) doesn't always make sense.

  1. Added to that, sending a text message that's as verbose as an HTML
     email is simply ridiculous. Each medium begets its own kind of
     content.
  2. Since, as we mentioned earlier, content should be manageable
     by non-programmers, the different ways of sending messages should
     be manageable by non-programmers.


I want it, stat!
----------------

Well, why don't you just head over to `the documentation`_ and we'll
get you started. A word of warning, it's not super simple to setup, but
it's worth it.


.. |pipeline-badge| image:: https://gitlab.com/alantrick/django-vox/badges/master/pipeline.svg
   :target: https://gitlab.com/alantrick/django-vox/
   :alt: Build Status

.. |coverage-badge| image:: https://gitlab.com/alantrick/django-vox/badges/master/coverage.svg
   :target: https://gitlab.com/alantrick/django-vox/
   :alt: Coverage Status

.. |docs-badge| image:: https://img.shields.io/badge/docs-latest-informational.svg
   :target: `the documentation`_
   :alt: Documentation

.. |pypi-badge| image:: https://img.shields.io/pypi/v/django_vox.svg
   :target: https://pypi.org/project/django-vox/
   :alt: Project on PyPI

.. _the documentation: https://alantrick.gitlab.io/django-vox/


CHANGES
=======

4.0
---

This version includes a new registration system for models so that you
don’t have to subclass ``VoxModel`` (which is a problem for 3rd party models).
The new way of registering the models is described in detail in the
documentation.

Incompatibilities with Version 3:

* The actor & target arguments on ``Notification.issue`` must be specified
  by keyword arguments now. This doesn’t affect
  ``VoxModel.issue_notification``, so it’s only relevant if you were manually
  loading Notifications and triggering them.
* A few default backends were are no longer defaults

Other changes:

* Backend settings can just reference the class, and not the module
* Notify will use a default address if none is specified
* Notifications now have a “last updated” field

3.6
---

* Fix bug in notification editor where switching one template's backend would
  alter the state of the another template form.
* Add more tests
* Make ``Backend.send_message`` an instance method, and instantiate backend
  objects when sending messages. This is a significant API change, but it's
  unlikely to actually cause backwards compatibility issues.
* Add title to notify page

3.5.3
-----

* Fix bugs in demo caused by slug
* Add icon

3.5.2
-----

* Add better support and testing for non-ID primary keys

3.5.1
-----

* Fix packaging problem (missing files)

3.5
---

* Fix some javascript problems on Django 2.1 & 2.2
* Add one-time message admin actions

3.4
---

* Fix crash when a non VoxModel model is registered

3.3
---

* Pin to a newer version of august, it works much better
* Be slightly more sophisticated with our activity data parsing

3.2
---

* fix implementation of activity\_type parameter
* Fix bug issuing notifications with non VoxModel objects
* Fix bug where django will crash if ``to_addresses`` is a generator
* Omit skipping message when notification is not from code
* Fix bug where we kept recreating notifications
* Keep orphaned notifications with templates so we don't delete data

3.1
---

* Add ability to remove notifications of deleted classes
* Fix error in notification editor when using grappelli

3.0
---

* Rewrite that add support for multiple participants

2.3
---

* add ``read_at`` field on inbox items
* Users should be posting read activities to outbox, duh

2.2
---

* Add the ability to post to inboxes and read messages

2.1
---

* Redo activity schema so that its more straightforward
* fix bug in ``background_task`` implementation

2.0.0
-----

* Add activity backend

1.1.0
-----

* Replace newlines in subject with space
* Add support for resending failed messages
* A few improvements to the admin
* Add Grappelli compatibility

1.0.0
-----

First stable release



