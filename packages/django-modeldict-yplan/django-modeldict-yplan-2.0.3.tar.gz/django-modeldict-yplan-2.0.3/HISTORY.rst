.. :changelog:

=======
History
=======

Pending release
---------------

.. Add new release notes below here

2.0.3 (2019-05-17)
------------------

* **Retired: this project is no longer maintained.** I (Adam Johnson) no longer
  have time to continue maintaining this. I was doing so to support
  `gargoyle-yplan <https://github.com/adamchainz/gargoyle>`__, a fork for my
  ex-employer YPlan. If you'd like to sponsor ongoing maintenance or take it
  over yourself, please contact me@adamj.eu.

2.0.2 (2019-04-28)
------------------

* Tested with Django 2.2. No changes were needed for compatibility.

2.0.1 (2019-02-15)
------------------

* No functional changes. This is a re-release of version 2.0.0 to fix immutable
  metadata on PyPI so that Pip on Python 2 doesn't pick up the Python 3 only
  2.X series. **Version 2.0.0 will be pulled from PyPI on 2019-03-01.**

2.0.0 (2019-01-29)
------------------

**This version is due to be pulled from PyPI, please use version 2.0.1 as per
its above release note.**

* Drop Python 2 support, only Python 3.4+ is supported now.
* Drop Django 1.8, 1.9, and 1.10 support. Only Django 1.11+ is supported now.
* Remove ``iteritems()``, ``iterkeys()``, and ``itervalues()`` methods from
  ``ModelDict``, and move ``items()``, ``keys()``, and ``values()`` to Python 3
  semantics, returning iterators rather than lists.
* Include LICENSE file in wheel.
* Tested with Django 2.1. No changes were needed for compatibility.

1.5.4 (2016-10-28)
------------------

* Fixed a race condition in threaded code. See https://github.com/adamchainz/django-modeldict/pull/40 for a detailed
  explanation. Thanks @Jaidan.

1.5.3 (2016-09-20)
------------------

* Stop rounding ``time.time()`` down to the nearest integer, so we are more fine grained around expiration. It might
  also fix a subtle timing bug around re-fetching the remote cache unnecessarily.

1.5.2 (2016-07-31)
------------------

* Fixed update missing when ``_local_last_updated`` could be set even when it
  wasn't updated
* Fixed update missing from integer rounding in time comparison
* Fixed ``CachedDict.__repr__`` so it works for other subclasses of
  ``CachedDict`` than ``ModelDict`` (don't assume ``self.model`` exists)

1.5.1 (2016-06-13)
------------------

* Fixed local cache never expiring if value was checked too often.
* Use Django's ``cache.set_many`` for more efficient storage.

1.5.0 (2016-01-11)
------------------

* Forked by YPlan
* Fixed concurrency TOCTTOU bug for threaded Django servers.
* Stopped including the 'tests' directory in package
* Django 1.8 and 1.9 supported.
* Python 3 support added.
* Fixed ``setdefault()`` to return the value that was set/found, as per normal dict semantics. Thanks @olevinsky.

1.4.1 (2012-12-04)
------------------

* Last release by Disqus
