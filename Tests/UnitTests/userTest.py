from django.test import TestCase
from classes import user

class test_getters(TestCase):
    def setUp(self):
        self.friendList = [user()]
        self.user = user("name", "email@uwm.edu", "password123", [3857], ["interests"], ["orgs"], ["majors"], self.friendList)
    
    def test_getName(self):
        self.assertEqual(self.user.getName(), "name")

    def test_getEmail(self):
        self.assertEqual(self.user.getEmail(), "email@uwm.edu")

    def test_getPassword(self):
        self.assertEqual(self.user.getPassword(), "password123")

    def test_getRoles(self):
        self.assertEqual(self.user.getRoles(), [3857])

    def test_getInterests(self):
        self.assertEqual(self.user.getInterests(), ["interests"])

    def test_getOrgs(self):
        self.assertEqual(self.user.getOrgs(), ["orgs"])

    def test_getMajors(self):
        self.assertEqual(self.user.getMajors(), ["majors"])

    def test_getFriends(self):
        self.assertEqual(self.user.getFriends(), self.friendList)

class test_setters(TestCase):
    def setUp(self):
        self.user = user()

    def test_setName(self):
        self.user.setName("name")
        self.assertEqual(self.user.getName(), "name")

    def test_setEmail(self):
        self.user.setEmail("email@uwm.edu")
        self.assertEqual(self.user.getEmail(), "email@uwm.edu")

    def test_setPassword(self):
        self.user.setPassword("password123")
        self.assertEqual(self.user.getPassword(), "password123")

    def test_setRoles(self):
        self.user.setRoles([123])
        self.assertEqual(self.user.getRoles(), [123])

    def test_setInterests(self):
        self.user.setInterests(["interests"])
        self.assertEqual(self.user.getInterests(), ["interests"])

    def test_setOrgs(self):
        self.user.setOrgs(["org"])
        self.assertEqual(self.user.getOrgs(), ["org"])

    def test_setMajors(self):
        self.user.setMajors(["majors"])
        self.assertEqual(self.user.getMajors(), ["majors"])

    def test_setFriends(self):
        self.userList2 = [user()]
        self.user.setFriends(self.userList2)
        self.assertEqual(self.user.getFriends(), self.userList2)
