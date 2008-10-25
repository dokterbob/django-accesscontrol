import logging

from socket import gethostbyaddr

from datetime import datetime, timedelta

from django.db import models
from django.utils.translation import ugettext_lazy as _

def is_blocked(ip, host=None, label=None, rate=None, timespan=None):
    """ Check whether a request is blocked by IP, host-name and maximum rate.
    
        Parameters:
        ip        -- The IP address of the request.
        host      -- The host name belonging to the specified IP.
                     If not set the host gets automatically resolved.
        label     -- A label for the kind of action performed for rate
                     blocking. This way we can use different maximum 
                     rates for different kinds of actions.
        rate      -- The maximum number of events for this label within timespan.
        timespan  -- The timespan over which the rate is calculated.
        
        If no host, label, rate or timespan is specified the default values
        for delegate functions BlockedIP.isBlocked, BlockedHost.isBlocked and 
        BlockRate.isBlocked are used.
    """
    if not host:
        host = gethostbyaddr(ip)[0]

    res =  BlockedIP.isBlocked(ip) or BlockedHost.isBlocked(host) or BlockRate.isBlocked(ip, label, rate, timespan)

    if not res:
        BlockRate.expireEvents(ip, label)
        BlockRate.addEvent(ip, label)

    return res

class BlockRate(models.Model):
    """ Block IP's by rate. """      
    ip = models.IPAddressField('IP', db_index=True, max_length=15)
    date_add = models.DateTimeField('datum', db_index=True, default=datetime.now(), blank=True, editable=False)
    label = models.CharField('label', default='default', db_index=True, max_length=15)

    def __str__(self):
        return '%s: %s' % (self.ip, self.date_add)
        
    @classmethod
    def addEvent(self, ip, label=None, date_add=None):
        o = BlockRate()
        o.ip = ip
        if date_add:
            o.date_add = date_add
        if label:
            o.label = label
        o.save()
    
    @classmethod
    def expireEvents(self, ip, timespan=None, label=None): 
        if not label:
            label='default'
            
        if not timespan:
            timespan=timedelta(hours=1)   
        
        starttime = datetime.now() - timespan
        q = self.objects.filter(date_add__lte=starttime)
        if label:
            q = q.filter(label__exact=label)
        
        q.delete()
    
    @classmethod
    def isBlocked(self, ip, label=None, rate=None, timespan=None):
        if not label:
            label='default'
            
        if not rate:
            rate=3
            
        if not timespan:
            timespan=timedelta(hours=1)
            
        starttime = datetime.now() - timespan
        
        q = self.objects.filter(ip__exact=ip, date_add__gte=starttime)
        if label:
            q = q.filter(label__exact=label)        
        
        num = q.count()
        
        if num > rate:
            logging.warn('accesscontrol: host blocked, rate exceeded')
            return True
        else:
            return False

class BlockedIP(models.Model):
    """ Block (partial) IP addresses. """
    ip = models.CharField('IP', db_index=True, max_length=15, unique=True, help_text=_("Use a %% sign for multi-character wildcards and a _ sign for a single wildcard character."))
    date_add = models.DateTimeField('datum', default=datetime.now(), blank=True, editable=False)

    def __str__(self):
        return self.ip

    @classmethod
    def isBlocked(self, ip):
        whereclause = "'%s' LIKE ip" % ip
        if self.objects.extra(where=[whereclause]).count():
            logging.warn('accesscontrol: host blocked, forbidden IP')
            return True
        else:
            return False

class BlockedHost(models.Model):
    """ Block (partial) hostnames. """
    host = models.CharField('hostnaam', db_index=True, max_length=255, unique=True, help_text="Use a %% sign for multi-character wildcards and a _ sign for a single wildcard character.")
    date_add = models.DateTimeField('datum', default=datetime.now(), blank=True, editable=False)

    def __str__(self):
        return self.host

    @classmethod
    def isBlocked(self, host):
        whereclause = "'%s' LIKE host" % host
        if self.objects.extra(where=[whereclause]).count():
            logging.warn('accesscontrol: host blocked, forbidden host')
            return True
        else:
            return False

