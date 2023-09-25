from django.test import TestCase
from django.test import Client

class test_setters(TestCase):
    def setUp(self):
        self.client = Client()

    def test_setName(self):
    
    def test_setOrg(self):

    def test_setLocation(self):

    def test_setDate(self):

    def test_setTime(self):

    def test_setDescription(self):

    def test_setEventType(self):

    def test_setViews(self):
        

class test_getters(TestCase):
    def setUp(self):
        self.client = Client()
        Event("name", "org","location","date","time","description", "event type", 1)

    def test_getName(self):
    
    def test_getOrg(self):

    def test_getLocation(self):

    def test_getDate(self):

    def test_getTime(self):

    def test_getDescription(self):

    def test_getEventType(self):

    def test_getViews(self):
