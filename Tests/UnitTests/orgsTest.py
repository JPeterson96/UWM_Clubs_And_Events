from django.test import TestCase
from classes import organization
from classes import user

class test_getters(TestCase):
    def setUp(self):
        self.org = organization("name", "Point of contact", 1, "description", 0, ["interest"])
        self.userList = [user()]
        self.club =  organization("name2", "Poc", 10, "description2", 1, ["interest2"], self.userList)

    def test_getName(self):
        self.assertEqual(self.org.getName(), "name")

    def test_getPointOfContact(self):
        self.assertEqual(self.org.getPointOfContact(), "Point of contact")

    def test_getNumberOfMembers(self):
        self.assertEqual(self.org.getNumberOfMembers(), 1)

    def test_getDescription(self):
        self.assertEqual(self.org.getDescription(), "description")

    def test_getRole(self):
        self.assertEqual(self.org.getRole(), 0)

    def test_getInterests(self):
        self.assertEqual(self.org.getInterests(), ["interest"])

    def test_getMembers(self):
        self.assertEqual(self.club.getMembers(), self.userList)


class test_setters(TestCase):
    def setUp(self):
        self.org = organization()

    def test_setName(self):
        self.org.setName("name")
        self.assertEqual(self.org.getName(), "name")

    def test_setPointOfContact(self):
        self.org.setPointOfContact("poc")
        self.assertEqual(self.org.getPointOfContact(), "poc")

    def test_setNumberOfMembers(self):
        self.org.setNumberOfMembers(1)
        self.assertEqual(self.org.getNumberOfMembers(), 1)

    def test_setDescription(self):
        self.org.setDescription("description")
        self.assertEqual(self.org.getDescription(), "description")

    def test_setRole(self):
        self.org.setRole(1)
        self.assertEqual(self.org.getRole(), 1)

    def test_setInterest(self):
        self.org.setInterest(["interest"])
        self.assertEqual(self.org.getInterest(), ["interest"])

    def test_setMembers(self):
        self.org.setMembers(["member"])
        self.assertEqual(self.org.getMembers(), ["member"])
        
