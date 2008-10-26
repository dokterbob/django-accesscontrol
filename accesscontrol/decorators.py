try:
    from functools import wraps
except ImportError:
    from django.utils.functional import wraps  # Python 2.3, 2.4 fallback.

from models import is_blocked
from django.core.exceptions import PermissionDenied

def limit_access(view_func, label=None, rate=None, timespan=None):
    """ 
    Decorator for limiting POST access to specific views. 
    
    Example usage:
    from accesscontrol.decorators import limit_access
    @limit_access
    def myview(request):
        <dosomething>
        
    Parameters:
    label     -- A label for the kind of action performed for rate
                 blocking. This way we can use different maximum 
                 rates for different kinds of actions.
                 Default: ACCESSCONTROL_DEFAULT_LABEL
    rate      -- The maximum number of events for this label within timespan.
    timespan  -- The timespan over which the rate is calculated.
    """
    
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.method == 'POST':
            params = {
                'ip'       : request.meta['REMOTE_ADDR'],
                'host'     : request.meta['REMOTE_HOST'],
                'label'    : label,
                'rate'     : rate,
                'timespan' : timespan
            }
            
            if is_blocked(**params):
                raise PermissionDenied
            
        return view_func(request, *args, **kwargs)
    
    return wrapper