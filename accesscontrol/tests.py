from django.test import TestCase

from models import *

class BlockedIPTestCase(TestCase):
    def setUp(self):
        BlockedIP(ip='10.0.0.1').save()
        BlockedIP(ip='123.234%').save()
        
    def testFull(self):
        self.assertEqual(BlockedIP.isBlocked('10.0.0.1'), True)
        self.assertEqual(BlockedIP.isBlocked('10.0.0.2'), False)
        
    def testPartial(self):
        self.assertEqual(BlockedIP.isBlocked('123.234.1.1'), True)
        self.assertEqual(BlockedIP.isBlocked('123.235.1.1'), False)
        
    def testOther(self):
        self.assertEqual(BlockedIP.isBlocked('192.168.1.1'), False)
        
class BlockedHostTestCase(TestCase):
    def setUp(self):
        BlockedHost(host='%%joepie%%').save()
        BlockedHost(host='pieter.xs4all.nl').save()
    
    def testFull(self):
        self.assertEqual(BlockedHost.isBlocked('pieter.xs4all.nl'), True)
        self.assertEqual(BlockedHost.isBlocked('jantje.xs4all.nl'), False)
        
    def testPartial(self):
        self.assertEqual(BlockedHost.isBlocked('joepie'), True)
        self.assertEqual(BlockedHost.isBlocked('jantje'), False)
        
    def testOther(self):
        self.assertEqual(BlockedHost.isBlocked('jantje'), False)    