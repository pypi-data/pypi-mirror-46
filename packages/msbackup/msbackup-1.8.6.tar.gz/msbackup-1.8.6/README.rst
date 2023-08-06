MSBackup utility
================

The *msbackup* utility performs data archiving.
The main use for this is the daily execution of the utility by system scheduler
(*cron* for example).

Usage
-----

For reliable archiving of various data have the appropriate backend:

* **file** - archive folder by the *tar* with optional compression
  and encryption;

* **hg** - scans the folder repositories of version control system
  `Mercurial
  <http://www.mercurial-scm.org/>`_ and executes the command *tar*
  with optional compression and encryption  on clone of each repository;

* **svn** - scans the folder repositories of version control system
  `Apache Subversion
  <http://subversion.apache.org/>`_ and archives each
  repository by the *tar* with optional compression and encryption  on dump
  of *hot copy* of each repository;

* **pg** - scans the relational database system
  `PostgreSQL
  <http://www.postgresql.org/>`_ cluster and archive each database with
  optional compression and encryption;

* **sqlite** - backup
  `SQLite
  <http://www.sqlite.org/>`_ database file with optional compression
  and encryption;

* **ldap** - backup
  `OpenLDAP
  <http://www.openldap.org/>`_ configuration and data with optional compression
  and encryption;

* **kvm** - online backup Qemu/KVN virtual machines with optional compression
  and encryption.

If you run the application with the --rotate option, the archives will be
rotated by adding a numeric extension to the file name.

Archive files can be encrypted with the *--encryptor gpg* parameter.

Build
-----

Before build Debian package install intto system project by URL
https://github.com/Aleksei-Badyaev/stdeb with command ::

   $ pip install -e git+https://github.com/Aleksei-Badyaev/stdeb.git\
   @ea98ce197a6a1262e85cd441feba7201b46af865#egg=stdeb

To build Debian package run the command::

   $ python setup.py --command-packages=stdeb.command bdist_deb

Testing
-------

Dependencies of this project can be installed by the command::

   $ pip install -U -e .[dev]

Tests can be launched by the command::

   $ python -m unittest discover -s src/test

Test reports and coverage report can be generate using::

   $ ./test.sh

After the successful execution of the script folder *test-reports* will contain
a report (in **XML** format) of the tests, and in the folder *coverage* will be
a report (in **HTML** format) of the code coverage.
