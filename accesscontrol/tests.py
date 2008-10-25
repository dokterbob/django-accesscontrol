from django.test import TestCase

from models import *

class BlockedIPTestCase(TestCase):
    def setUp(self):
        BlockedIP(ip='10.0.0.1').save()
        BlockedIP(ip='123.234%').save()
    
    def testFull(self):
        self.assertEqual(BlockedIP.isBlocked('10.0.0.1'), True)
        
    def testPartial(self):
        self.assertEqual(BlockedIP.isBlocked('123.234.1.1'), True)
        
    def testOther(self):
        self.assertEqual(BlockedIP.isBlocked('192.168.1.1'), False)
        
