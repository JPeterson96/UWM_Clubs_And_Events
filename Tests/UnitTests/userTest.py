from django.test import TestCase
from django.test import Client

class test_setters(TestCase):
    def setUp(self):
        self.client = Client()

    def test_setName(self):

    def test_setEmail(self):

    def test_setPassword(self):

    def test_setRoles(self):

    def test_setInterests(self):

    def test_setOrgs(self):

    def test_setMajors(self):

    def test_setFriends(self):

class test_getters(TestCase):
    def setUp(self):
        self.client = Client()
        User("name", "email@uwm.edu", "password123", [3857], ["interests"], ["orgs"], ["majors"], [User()])
    
    def test_getName(self):

    def test_getEmail(self):

    def test_getPassword(self):

    def test_getRoles(self):

    def test_getInterests(self):

    def test_getOrgs(self):

    def test_getMajors(self):

    def test_getFriends(self):
