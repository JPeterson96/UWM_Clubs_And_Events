from django.test import TestCase
from classes.user_util import User_Util as user_util

class TestCreateUser(TestCase):

    def test_createUser(self):
        self.made = user_util.create_user(name = "Ilya", email = "kravtso5@uwm.edu", password = "123")
        self.assertEqual(self.made, True)

        self.user = user_util.get_user("kravtso5@uwm.edu")
        self.assertEqual(self.user.name , "Ilya")
        self.assertEqual(self.user.password , "123")

class TestInvalidInput(TestCase):

    def test_emptyName(self):
        self.made = user_util.create_user(name = "", email = "kravtso5@uwm.edu", password = "123")
        self.assertEqual(self.made, False)

    def test_emptyEmail(self):
        self.made = user_util.create_user(name = "Ilya", email = "", password = "123")
        self.assertEqual(self.made, False)

    def test_emptyPassword(self):
        self.made = user_util.create_user(name = "Ilya", email = "kravtso5@uwm.edu", password = "")
        self.assertEqual(self.made, False)

    def test_invalidEmail(self):
        self.made = user_util.create_user(name = "Bob", email = "invalid email", password = "123")
        self.assertEqual(self.made, False)