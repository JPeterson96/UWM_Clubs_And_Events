from django.test import TestCase
from classes.user_util import User_Util as user_util
from UWM_Clubs_and_Events.models import User

class TestAddFriend(TestCase):
    def test_addFriend(self):
        self.user = User(name = "Ilya", email = "kravtso5@uwm.edu", password = "123", role = 0)
        self.user.save()
        self.user2 = User(name = "Omar", email = "aburmai2@uwm.edu", password = "123", role = 0)
        self.user2.save()
        self.assertTrue(user_util.add_friend("kravtso5@uwm.edu", "aburmai2@uwm.edu"), "Friend should have been added")

class TestAddFriendInvalid(TestCase):
    def test_addFriendInvalid(self):
        self.user = User(name = "Ilya", email = "kravtso5@uwm.edu", password = "123", role = 0)
        self.user.save()
        self.assertFalse(user_util.add_friend("kravtso5@uwm.edu", "aburmai2@uwm.edu"), "Friend should not have been added")

class TestRemoveFriend(TestCase):
    def test_removeFriend(self):
        self.user = User(name = "Ilya", email = "kravtso5@uwm.edu", password = "123", role = 0)
        self.user.save()
        self.user2 = User(name = "Omar", email = "aburmai2@uwm.edu", password = "123", role = 0)
        self.user2.save()
        user_util.add_friend("kravtso5@uwm.edu", "aburmai2@uwm.edu")
        self.assertTrue(user_util.remove_friend("kravtso5@uwm.edu", "aburmai2@uwm.edu"), "Friend should have been removed")

class TestRemoveFriendInvalid(TestCase):
    def test_removeFriendInvalid(self):
        self.user = User(name = "Ilya", email = "kravtso5@uwm.edu", password = "123", role = 0)
        self.user.save()
        self.assertFalse(user_util.remove_friend("kravtso5@uwm.edu", "aburmai2@uwm.edu"), "Friend should not have been removed")

class TestGetFriends(TestCase):
    def test_getFriends(self):
        self.user = User(name = "Ilya", email = "kravtso5@uwm.edu", password = "123", role = 0)
        self.user.save()
        self.user2 = User(name = "Omar", email = "kravtso5@uwm.edu", password = "123", role = 0)
        self.user2.save()
        user_util.add_friend("kravsto5@uwm.edu", "aburmai2@uwm.edu")
        self.assertTrue(self.user2 in user_util.get_friends("kravtso5@uwm.edu"), "Friend should have been found")

class TestGetFriendsInvalid(TestCase):
    def test_getFriendsInvalid(self):
        self.assertFalse(user_util.get_friends("nonexistant@uwm.edu").exists(), "No friends should have been found")


                         