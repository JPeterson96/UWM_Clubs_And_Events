from django.test import TestCase
from classes.user_util import User_Util as user_util
import datetime

class TestCreateUser(TestCase):

    def test_createUser(self):
        self.time = datetime.datetime(year=2020, month=1, day=1, hour=0, minute=0, second=0, tzinfo = datetime.timezone.utc)
        made = user_util.create_user(name = "Ilya", email = "kravtso5@uwm.edu", password = "123", role = 0, 
                                     startdate = self.time, graddate = self.time)
        self.assertEqual(made, True, msg="User should have been created, returned false")

        self.user = user_util.get_user("kravtso5@uwm.edu")
        self.assertEqual(self.user.name , "Ilya")
        self.assertEqual(self.user.password , "123")
        self.assertEqual(self.user.role , 0)

class TestInvalidInput(TestCase):

    def setUp(self):
        self.time = datetime.datetime(year=2020, month=1, day=1, hour=0, minute=0, second=0, tzinfo = datetime.timezone.utc)

    def test_emptyName(self):
        with self.assertRaises(ValueError, msg="Missing Name"):
            self.test = user_util.create_user(name="", email = "kravtso5@uwm.edu", password = "123", role= 0, 
                                              startdate = self.time, graddate = self.time)

    def test_emptyEmail(self):
        with self.assertRaises(ValueError, msg="Missing Email"):
            self.test = user_util.create_user(name = "test", email="", password = "123", role=0, 
                                              startdate = self.time, graddate = self.time)

    def test_emptyPassword(self):
        with self.assertRaises(ValueError, msg="Missing Password"):
            self.test = user_util.create_user(name = "test", email = "kravtso5@uwm.edu", password="", role=0, 
                                              startdate = self.time, graddate = self.time)

    def test_invalidEmail(self):
        with self.assertRaises(ValueError, msg="Invalid Email"):
            self.test = user_util.create_user(name = "test", email = "kravtsov", password = "123", role=0, 
                                              startdate = self.time, graddate = self.time)

    def test_invalidRole(self):
        with self.assertRaises(ValueError, msg="Invalid Role"):
            self.test = user_util.create_user(name="test", email="kravtso5@uwm.edu", password="123", role=99, 
                                              startdate = self.time, graddate = self.time)

