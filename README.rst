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

Usage
=====
For now there exists an (**untested**) decorator for limiting POST access to
specific views. If access is not allowed a 403 (Forbidden) error code is
returned. The template for this page is called 403.html, consistent with error
handling in Django.

Example usage:
from accesscontrol.decorators import limit_access

@limit_access(**parameters)
def myview(request):
    <dosomething>
    
Parameters:
label     -- A label for the kind of action performed for rate
             blocking. This way we can use different maximum 
             rates for different kinds of actions.
             Default: ACCESSCONTROL_DEFAULT_LABEL
rate      -- The maximum number of events for this label within timespan.
timespan  -- The timespan over which the rate is calculated.

Configuration variables
=======================
* DEFAULT_LABEL [default]  --  Default label for rate control mechanism.
* AUTO_EXPIRE [True]       --  Automatically expire events when executing
                               BlockRate.isBlocked().

License
=======
This product is released under the GPL version 3.