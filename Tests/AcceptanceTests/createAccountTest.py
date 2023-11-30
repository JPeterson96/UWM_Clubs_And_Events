from django.test import TestCase
from django.test import Client
from UWM_Clubs_and_Events.models import User
from classes.user_util import User_Util as user_util
from UWM_Clubs_and_Events.models import Interest
from UWM_Clubs_and_Events.models import Major


class TestCreateValidUser(TestCase):
    def setUp(self):
        self.client = Client()
        self.interest = Interest.objects.create(tag="Computer Science")
        self.major = Major.objects.create(name="Computer Science")

    def test_createUser(self):
        self.resp = self.client.post("/createAccount/", {"firstname": "Ilya", "lastname": "Kravtsov", 
                                                      "email": "kravtso5@uwm.edu", "password": "password", 
                                                      "majorlist": "Computer Science", "selected_interests": "Computer Science", 
                                                      "startdate": "2021-09-01", "graddate": "2021-12-01"})
        self.assertEqual(self.resp.status_code, 200)
        self.assertEquals(self.resp.context["success_message"], "user account successfully created")
        self.assertIsNotNone(user_util.get_user("kravtso5@uwm.edu"))

class TestCreateInvalidUser(TestCase):

    def setUp(self):
        self.client = Client()
        self.interest = Interest.objects.create(tag="Computer Science")
        self.major = Major.objects.create(name="Computer Science")

    def test_createUserEmptyFirstName(self):
        self.resp = self.client.post("/createAccount/", {"firstname": "", "lastname": "Kravtsov", 
                                                      "email": "kravtso5@uwm.edu", "password": "password",
                                                        "majorlist": "Computer Science", "selected_interests": "Computer Science",
                                                        "startdate": "2021-09-01", "graddate": "2021-12-01"})
        self.assertEqual(self.resp.status_code, 200)
        self.assertEquals(self.resp.context["message"], "First Name Field Empty")
        self.assertIsNone(user_util.get_user("kravtso5@uwm.edu"))

    def test_createUserEmptyLastName(self):
        self.resp = self.client.post("/createAccount/", {"firstname": "Ilya", "lastname": "", 
                                                      "email": "kravtso5@uwm.edu", "password": "password",
                                                        "majorlist": "Computer Science", "selected_interests": "Computer Science",
                                                        "startdate": "2021-09-01", "graddate": "2021-12-01"})
        self.assertEqual(self.resp.status_code, 200)
        self.assertEquals(self.resp.context["message"], "Last Name Field Empty")
        self.assertIsNone(user_util.get_user("kravtso5@uwm.edu"))

    def test_createUserEmptyPassword(self):
        self.resp = self.client.post("/createAccount/", {"firstname": "Ilya", "lastname": "Kravtsov", 
                                                      "email": "kravtso5@uwm.edu", "password": "",
                                                        "majorlist": "Computer Science", "selected_interests": "Computer Science",
                                                        "startdate": "2021-09-01", "graddate": "2021-12-01"})
        self.assertEqual(self.resp.status_code, 200)
        self.assertEquals(self.resp.context["message"], "Password Field Empty")
        self.assertIsNone(user_util.get_user("kravtso5@uwm.edu"))

    def test_createUserEmptyEmail(self):
        self.resp = self.client.post("/createAccount/", {"firstname": "Ilya", "lastname": "Kravtsov", 
                                                      "email": "", "password": "password",
                                                        "majorlist": "Computer Science", "selected_interests": "Computer Science",
                                                        "startdate": "2021-09-01", "graddate": "2021-12-01"})
        self.assertEqual(self.resp.status_code, 200)
        self.assertEquals(self.resp.context["message"], "Email Field Empty")

    def test_createUserEmptyMajor(self):
        self.resp = self.client.post("/createAccount/", {"firstname": "Ilya", "lastname": "Kravtsov", 
                                                      "email": "kravtso5@uwm.edu", "password": "password",
                                                        "majorlist": "", "selected_interests": "Computer Science",
                                                        "startdate": "2021-09-01", "graddate": "2021-12-01"})
        self.assertEqual(self.resp.status_code, 200)
        self.assertEquals(self.resp.context["message"], "Major Field Empty")
        self.assertIsNone(user_util.get_user("kravtso5@uwm.edu"))

    def test_createUserEmptyInterest(self):
        self.resp = self.client.post("/createAccount/", {"firstname": "Ilya", "lastname": "Kravtsov", 
                                                      "email": "kravtso5@uwm.edu", "password": "password",
                                                        "majorlist": "Computer Science", "selected_interests": "",
                                                        "startdate": "2021-09-01", "graddate": "2021-12-01"})
        self.assertEqual(self.resp.status_code, 200)
        self.assertEquals(self.resp.context["message"], "Interest Field Empty")
        self.assertIsNone(user_util.get_user("kravtso5@uwm.edu"))

    def test_createUserEmptyStartDate(self):
        self.resp = self.client.post("/createAccount/", {"firstname": "Ilya", "lastname": "Kravtsov", 
                                                      "email": "kravtso5@uwm.edu", "password": "password",
                                                        "majorlist": "Computer Science", "selected_interests": "Computer Science",
                                                        "startdate": "", "graddate": "2021-12-01"})
        self.assertEqual(self.resp.status_code, 200)
        self.assertEquals(self.resp.context["message"], "Start Date Field Empty")
        self.assertIsNone(user_util.get_user("kravtso5@uwm.edu"))

    def test_createUserEmptyGradDate(self):
        self.resp = self.client.post("/createAccount/", {"firstname": "Ilya", "lastname": "Kravtsov", 
                                                      "email": "kravtso5@uwm.edu", "password": "password",
                                                        "majorlist": "Computer Science", "selected_interests": "Computer Science",
                                                        "startdate": "2021-09-01", "graddate": ""})
        self.assertEqual(self.resp.status_code, 200)
        self.assertEquals(self.resp.context["message"], "Grad Date Field Empty")
        self.assertIsNone(user_util.get_user("kravtso5@uwm.edu"))

class TestCreateUserWithExistingEmail(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.interest = Interest.objects.create(tag="Computer Science")
        self.major = Major.objects.create(name="Computer Science")
        self.user = User.objects.create(name="Ilya Kravtsov", email="kravtso5@uwm.edu", password="password", 
                                            major=self.major, start_date="2021-09-01", grad_date="2021-12-01")
            
    def test_createUser(self):
        self.resp = self.client.post("/createAccount/", {"firstname": "Ilya", "lastname": "Kravtsov", 
                                                      "email": "kravtso5@uwm.edu", "password": "password",
                                                        "majorlist": "Computer Science", "selected_interests": "Computer Science",
                                                        "startdate": "2021-09-01", "graddate": "2021-12-01"})
        
        self.assertEqual(self.resp.status_code, 200)
        self.assertEquals(self.resp.context["message"], "user with email exists")

class TestCreateUserWithInvalidEmail(TestCase):
        
    def setUp(self):
        self.client = Client()
        self.interest = Interest.objects.create(tag="Computer Science")
        self.major = Major.objects.create(name="Computer Science")
        
    def test_createUser(self):
        self.resp = self.client.post("/createAccount/", {"firstname": "Ilya", "lastname": "Kravtsov", 
                                                      "email": "kravtso5", "password": "password",
                                                        "majorlist": "Computer Science", "selected_interests": "Computer Science",
                                                        "startdate": "2021-09-01", "graddate": "2021-12-01"})
        
        self.assertEqual(self.resp.status_code, 200)
        self.assertEquals(self.resp.context["message"], "Invalid Email")