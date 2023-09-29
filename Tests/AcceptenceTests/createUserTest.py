from django.test import TestCase
from django.test import Client
from UWM_Clubs_and_Events.models import User

class TestCreateValidUser(TestCase):
    def setUp(self):
        self.client = Client()

    def test_createUser(self):
        self.resp = self.client.post("/createuser/", {"name": "Ilya Kravtsov", "email": "kravtso5@uwm.edu",
                                     "password": "123456"}, follow=True)
        self.assertEqual("Success: New Account has been created", self.resp.context["msg"],
                         "Failed creation. One or more fields invalid")

class TestCreateInvalid(TestCase):
    def setUp(self):
        self.client = Client()

    def test_emptyFields(self):
        self.resp = self.client.post("/createuser/", {"name": "", "email": "",
                                     "password": ""}, follow=True)
        self.assertEqual("Error: One or more fields invalid", self.resp.context["msg"],
                         "User created with one or more fields empty")

    def test_blankField(self):
        self.resp = self.client.post("/createuser/", {"name": " ", "email": " ",
                                    "password": " "}, follow=True)
        self.assertEqual("Error: One or more fields invalid", self.resp.context["msg"],
                         "User created with one or more fields blank")

    def test_duplicateUser(self):
        self.user = User(name = "Ilya", email  ="kravtso5@uwm.edu", password = "123456", role = 0)
        self.user.save()
        self.resp = self.client.post("/createuser/", {"name": "Ilya", "email": "kravtso5@uwm.edu",
                                     "password":"123456"}, follow=True)
        self.assertEqual("Error: One or more fields invalid", self.resp.context["msg"],
                         "Duplicate user created")

    