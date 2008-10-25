from django.test import TestCase

from models import *

class BlockedIPTestCase(TestCase):
    def setUp(self):
        BlockedIP(ip='10.0.0.1').save()
        BlockedIP(ip='123.234%').save()
        
    def testFull(self):
        self.assert_(BlockedIP.isBlocked('10.0.0.1'))
        self.assertEqual(BlockedIP.isBlocked('10.0.0.2'), False)
        
    def testPartial(self):
        self.assert_(BlockedIP.isBlocked('123.234.1.1'))
        self.assertEqual(BlockedIP.isBlocked('123.235.1.1'), False)
        
    def testOther(self):
        self.assertEqual(BlockedIP.isBlocked('192.168.1.1'), False)
        
class BlockedHostTestCase(TestCase):
    def setUp(self):
        BlockedHost(host='%%joepie%%').save()
        BlockedHost(host='pieter.xs4all.nl').save()
    
    def testFull(self):
        self.assert_(BlockedHost.isBlocked('pieter.xs4all.nl'))
        self.assertEqual(BlockedHost.isBlocked('jantje.xs4all.nl'), False)
        
    def testPartial(self):
        self.assert_(BlockedHost.isBlocked('joepie'))
        self.assertEqual(BlockedHost.isBlocked('jantje'), False)
        
    def testOther(self):
        self.assertEqual(BlockedHost.isBlocked('jantje'), False)

from datetime import timedelta
from time import time #, sleep
        
class BlockRateTestCase(TestCase):
    def setUp(self):
        # Add 10 consecutive events quickly after one another
        self.ip = '10.0.0.1'
        self.rate = 10
        self.start = time()
        for a in range(1, self.rate + 1):
            BlockRate.addEvent(self.ip)
            #sleep(1)
                    
    def testRate(self):
        self.assert_(BlockRate.isBlocked(self.ip, rate=self.rate-1, timespan=timedelta(seconds=time() - self.start)))
        self.failIf(BlockRate.isBlocked(self.ip, rate=self.rate+1, timespan=timedelta(seconds=time() - self.start)))
        
    def testTimespan(self):
        self.assert_(BlockRate.isBlocked(self.ip, rate=self.rate, timespan=timedelta(seconds=time() - self.start + 1)))
        self.failIf(BlockRate.isBlocked(self.ip, rate=self.rate, timespan=timedelta(seconds=0)))
