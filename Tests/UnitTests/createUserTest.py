from django.test import TestCase
from classes.user_util import User_Util as user_util

class TestCreateUser(TestCase):

    def test_createUser(self):
        made = user_util.create_user(name = "Ilya", email = "kravtso5@uwm.edu", password = "123", role = 0)
        self.assertEqual(made, True, msg="User should have been created, returned false")

        self.user = user_util.get_user("kravtso5@uwm.edu")
        self.assertEqual(self.user.name , "Ilya")
        self.assertEqual(self.user.password , "123")

class TestInvalidInput(TestCase):

    def test_emptyName(self):
        with self.assertRaises(TypeError, msg="Missing Name"):
            self.test = user_util.create_user(email = "kravtso5@uwm.edu", password = "123", role= 0)

    def test_emptyEmail(self):
        with self.assertRaises(TypeError, msg="Missing Email"):
            self.test = user_util.create_user(name = "test", password = "123", role= 0)

    def test_emptyPassword(self):
        with self.assertRaises(TypeError, msg="Missing Password"):
            self.test = user_util.create_user(name="test", email = "kravtso5@uwm.edu", role= 0)

    def test_invalidEmail(self):
        with self.assertRaises(TypeError, msg="Missing role"):
            self.test = user_util.create_user(name="test", email = "kravtso5", password = "123")
