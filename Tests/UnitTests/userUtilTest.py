from django.test import TestCase
from classes.user_util import User_Util
from UWM_Clubs_and_Events.models import User

class TestGetUser(TestCase):
    
    def test_getUserValid(self):
        self.user = User(name = "Ilya", email = "kravtso5@uwm.edu", password = "123", role = 0)
        self.user.save()
        self.assertEqual(User_Util.get_user("kravtso5@uwm.edu"), self.user, "User should have been found")

class TestGetUserInvalid(TestCase):
    def test_getUserInvalid(self):
        self.assertEqual(User_Util.get_user("kravtso5@uwm.edu"), None, "User should not have been found")

class TestGetAllUsers(TestCase):
    def test_getAllUsers(self):
        self.user = User()
        self.user.save()
        self.assertTrue(self.user in User_Util.get_all_users(), "User should have been found in all users")

class TestGetUserByName(TestCase):
    def test_getUserByName(self):
        self.user = User(name = "Ilya")
        self.user.save()
        self.assertTrue(self.user in User_Util.get_user_by_name("Ilya"), "Users should have been found by name")

class TestGetUserByNameInvalid(TestCase):
    def test_getUserByNameInvalid(self):
        self.assertFalse(User_Util.get_user_by_name("NonExistent").exists(), "No users should have been found")

class TestGetUsersByMajor(TestCase):
    def test_getUsersByMajor(self):
        self.user = User(major = "CS")
        self.user.save()
        self.assertTrue(self.user in User_Util.get_users_by_major("CS"), "Users should have been found by major")

class TestGetUsersByMajorInvalid(TestCase):
    def test_getUsersByMajorInvalid(self):
        self.assertFalse(User_Util.get_users_by_major("NonExistent").exists(), "No users should have been found")

class TestGetUsersByInterest(TestCase):
    def test_getUsersByInterest(self):
        self.user = User(interests = "CS")
        self.user.save()
        self.assertTrue(self.user in User_Util.get_users_by_interest("CS"), "Users should have been found by interest")

class TestGetUsersByInterestInvalid(TestCase):
    def test_getUsersByInterestInvalid(self):
        self.assertFalse(User_Util.get_users_by_interest("NonExistent").exists(), "No users should have been found")