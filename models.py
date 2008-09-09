from django.db import models

from socket import gethostbyaddr

from datetime import datetime, timedelta

def is_blocked(ip, host=None, label=None, rate=None, timespan=None):
    if not host:
        host = gethostbyaddr(ip)[0]

    res =  BlockedIP.isBlocked(ip) or BlockedHost.isBlocked(host) or BlockRate.isBlocked(ip, label, rate, timespan)

    if not res:
        BlockRate.expireEvents(ip, label)
        BlockRate.addEvent(ip, label)

    return res

class BlockRate(models.Model):
    class Admin:
        pass
        
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
            print 'rate exceeded'
            return True
        else:
            return False

class BlockedIP(models.Model):
    class Admin:
        pass

    ip = models.CharField('IP', db_index=True, max_length=15, unique=True)
    date_add = models.DateTimeField('datum', default=datetime.now(), blank=True, editable=False)

    def __str__(self):
        return self.ip

    @classmethod
    def isBlocked(self, ip):
        if self.objects.extra(where=["LOCATE(ip,'%s')" % ip]).count():
            print 'host blocked'
            return True
        else:
            return False

class BlockedHost(models.Model):
    class Admin:
        pass

    host = models.CharField('hostnaam', db_index=True, max_length=200, unique=True)
    date_add = models.DateTimeField('datum', default=datetime.now(), blank=True, editable=False)

    def __str__(self):
        return self.host

    @classmethod
    def isBlocked(self, host):
        if self.objects.extra(where=["LOCATE(host,'%s')" % host]).count():
            print 'IP blocked'
            return True
        else:
            return False

