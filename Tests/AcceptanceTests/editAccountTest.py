from django.test import TestCase
from django.test import Client
from classes.user_util import User_Util as user_util
from UWM_Clubs_and_Events.models import Interest
from UWM_Clubs_and_Events.models import Major
from UWM_Clubs_and_Events.models import StudentMajor
from UWM_Clubs_and_Events.models import StudentInterest
from django.db.models import Q

class TestValidEditUser(TestCase):
    def setUp(self):
        self.client = Client()
        self.interest = Interest.objects.create(tag="Computer Science")
        self.major = Major.objects.create(name="Computer Science")
        self.interest2 = Interest.objects.create(tag="Music")
        self.major2 = Major.objects.create(name="Music")
        self.client.post("/createAccount/", {"firstname": "Ilya", "lastname": "Kravtsov", 
                                                      "email": "kravtso5@uwm.edu", "password": "123", 
                                                      "majorlist": "Computer Science", "selected_interests": "Computer Science", 
                                                      "startdate": "2021-09-01", "graddate": "2021-12-01"})
        self.user = user_util.get_student("kravtso5@uwm.edu")
        self.client.post("/", {"email": "kravtso5@uwm.edu", "password": "123"})

    def test_editUser(self):
        self.resp = self.client.post('/viewaccount/editaccount', {"firstname": "Alex", "lastname": "Chestnut", 
                                                      "majorremoval": "Computer Science", "majorlist": "Music", 
                                                      "interestremoval": "Computer Science", "interesttoadd": "Music",
                                                        "startdate": "2021-09-01", "graddate": "2023-01-12", "password": "1234"})
        self.assertEquals(self.resp.status_code, 200)
        self.assertEquals(self.resp.context["message"], "user sucessfully edited")
        self.assertEquals(self.user.user.name, "Alex Chestnut")
        self.assertIsNotNone(StudentMajor.objects.filter(Q(student=self.user, major=self.major2)))
        self.assertIsNotNone(StudentInterest.objects.filter(Q(student=self.user, type=self.interest2)))
        self.assertEquals(self.user.user.password, "1234")

class TestInvalidEditUser(TestCase):
    def setUp(self):
        self.client = Client()
        self.interest = Interest.objects.create(tag="Computer Science")
        self.major = Major.objects.create(name="Computer Science")
        self.interest2 = Interest.objects.create(tag="Music")
        self.major2 = Major.objects.create(name="Music")
        self.client.post("/createAccount/", {"firstname": "Ilya", "lastname": "Kravtsov", 
                                                      "email": "kravtso5@uwm.edu", "password": "123", 
                                                      "majorlist": "Computer Science", "selected_interests": "Computer Science", 
                                                      "startdate": "2021-09-01", "graddate": "2021-12-01"})
        self.user = user_util.get_student("kravtso5@uwm.edu")
        self.client.post("/", {"email": "kravtso5@uwm.edu", "password": "123"})

    def test_editUserNoFirstName(self):
        self.resp = self.client.post('/viewaccount/editaccount', {"firstname": "", "lastname": "Chestnut", 
                                                      "majorremoval": "Computer Science", "majorlist": "Music", 
                                                      "interestremoval": "Computer Science", "interesttoadd": "Music",
                                                        "startdate": "2021-09-01", "graddate": "2023-01-12", "password": "1234"})
        self.assertEquals(self.resp.context["message"], "user failed to edit")

    def test_editUserNoLastName(self):
        self.resp = self.client.post('/viewaccount/editaccount', {"firstname": "Alex", "lastname": "", 
                                                      "majorremoval": "Computer Science", "majorlist": "Music", 
                                                      "interestremoval": "Computer Science", "interesttoadd": "Music",
                                                        "startdate": "2021-09-01", "graddate": "2023-01-12", "password": "1234"})
        self.assertEquals(self.resp.context["message"], "user failed to edit")

    def test_duplicateMajor(self):
        self.resp = self.client.post('/viewaccount/editaccount', {"firstname": "Alex", "lastname": "Chestnut", 
                                                                  "majorlist": "Computer Science", 
                                                      "interestremoval": "Computer Science", "interesttoadd": "Music",
                                                        "startdate": "2021-09-01", "graddate": "2023-01-12", "password": "1234"})
        self.assertEquals(StudentMajor.objects.filter(Q(student=self.user, major=self.major)).count(), 1)

    def test_duplicateInterest(self):
        self.resp = self.client.post('/viewaccount/editaccount', {"firstname": "Alex", "lastname": "Chestnut", 
                                                                  "majorremoval": "Computer Science", "majorlist": "Music", 
                                                      "interesttoadd": "Computer Science",
                                                        "startdate": "2021-09-01", "graddate": "2023-01-12", "password": "1234"})
        self.assertEquals(StudentInterest.objects.filter(Q(student=self.user, type=self.interest)).count(), 1)

    def test_emptyPassword(self):
        self.resp = self.client.post('/viewaccount/editaccount', {"firstname": "Alex", "lastname": "Chestnut", 
                                                                  "majorremoval": "Computer Science", "majorlist": "Music", 
                                                      "interestremoval": "Computer Science", "interesttoadd": "Music",
                                                        "startdate": "2021-09-01", "graddate": "2023-01-12", "password": ""})
        self.assertEquals(self.resp.context["message"], "user failed to edit")