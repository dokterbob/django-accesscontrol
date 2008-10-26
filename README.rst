====================
django-accesscontrol
====================

What is it?
===========
Django-accesscontrol is pluggable Django 1.0+ application for limiting
access by IP (fragment), hostname(fragment) and access rate.

Status
======
This product can be considered as beta. The code *should* be stable
enough for production use but it has not been sufficiently tested.

Also, the API still requires a fair amount of documentation. Until that
time, taking a look at models.py and tests.py should provide a good start.

Configuration variables
=======================
* DEFAULT_LABEL     [default]
  Default label for rate control mechanism.

* AUTO_EXPIRE       [True]
  Automatically expire events when executing BlockRate.isBlocked().

License
=======
This product is released under the GPL version 3.