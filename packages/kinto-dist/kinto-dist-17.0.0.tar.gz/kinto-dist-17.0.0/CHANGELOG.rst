CHANGELOG
#########

This document describes changes between each past release as well as
the version control of each dependency.


17.0.0 (2019-05-27)
===================

kinto
-----

**kinto 12.0.1 → 13.1.1**: https://github.com/Kinto/kinto/releases/tag/13.1.1

**Breaking changes**

- Update Kinto OpenID plugin to redirect with a base64 JSON encoded token. (#1988).
  *This will work with kinto-admin 1.23*

**New features**

- Expose the user_profile in the user field of the hello page. (#1989)
- Add an "account validation" option to the accounts plugin. (#1973)
- Add a ``validate`` endpoint at ``/accounts/{user id}/validate/{validation
  key}`` which can be used to validate an account when the *account
  validation* option is enabled on the accounts plugin.
- Add a ``reset-password`` endpoint at ``/accounts/(user
  id)/reset-password`` which can be used to reset a user's password when the
  *account validation* option is enabled on the accounts plugin.

**Bug fixes**

- Fix cache heartbeat test (fixes Kinto/kinto#2107)
- Fix support of ``sqlalchemy.pool.NullPool`` for PostgreSQL backends.
  The default ``pool_size`` of 25 is maintained on the default pool class
  (``QueuePoolWithMaxBacklog``). When using custom connection pools, please
  refer to SQLAlchemy documentation for default values.
- Fixed two potential bugs relating to mutable default values.
- Fix crash on validating records with errors in arrays (#1508)
- Fix crash on deleting multiple accounts (#2009)
- Loosen up the Content-Security policies in the Kinto Admin plugin to prevent Webpack inline script to be rejected (fixes #2000)
- **security**: Fix a pagination bug in the PostgreSQL backend that could leak records between collections

kinto-redis
-----------

**kinto-redis 2.0.0 → 2.0.1**: https://github.com/Kinto/kinto-redis/releases/tag/2.0.1

**Bug fixes**

- ``pool_size`` setting should remain optional

