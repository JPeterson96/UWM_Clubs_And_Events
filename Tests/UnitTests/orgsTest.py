from django.test import TestCase
from django.test import Client

class test_setters(TestCase):
    def setUp(self):
        self.client = Client()

    def test_setName(self):

    def test_setPointOfContact(self):

    def test_setNumberOfMembers(self):

    def test_setDescription(self):

    def test_setRole(self):

    def test_setMembers(self):
        

class test_getters(TestCase):
    def setUp(self):
        self.client = Client()
        Organization org = Organization("name", "Point of contact", 1, "description", 0, ["interest"])
        Organization club =  Organization("name2", "Poc", 10, "description2", 1, ["interest2"], [User()])

    def test_getName(self):

    def test_getPointOfContact(self):

    def test_getNumberOfMembers(self):

    def test_getDescription(self):

    def test_getRole(self):

    def test_getMembers(self):
