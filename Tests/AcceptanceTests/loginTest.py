from django.test import TestCase
from django.test import Client
from UWM_Clubs_and_Events.models import User

class SuccessfulLogin(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User(name = "Ilya", email = "kravtso5@uwm.edu", password = "123", role = 0)
        self.user.save()
    
    def test_successfulLogin(self):
        resp = self.client.post("/", {"email": "kravtso5@uwm.edu", "password": "123"})
        self.assertEqual(resp.status_code, 302, "Login should have been successful")

class UnsuccessfulLogin(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User(name = "Ilya", email = "kravtso5@uwm.edu", password = "123", role = 0)
        self.user.save()

    def test_wrongPassword(self):
        resp = self.client.post("/", {"email": "kravtso5@uwm.edu", "password": "1234"})
        self.assertEqual(resp.status_code, 200, "Login should have failed, wrong password")

    def test_wrongEmail(self):
        resp = self.client.post("/", {"email": "kravtsov@uwm.edu", "password": "123"})
        self.assertEqual(resp.status_code, 200, "Login should have failed, wrong email")

    def test_wrongEmailAndPassword(self):
        resp = self.client.post("/", {"email": "kravtsov@uwm.edu", "password": "1234"})
        self.assertEqual(resp.status_code, 200, "Login should have failed, wrong email and password")

    def test_noEmail(self):
        resp = self.client.post("/", {"email": "", "password": "123"})
        self.assertEqual(resp.status_code, 200, "Login should have failed, no email")

    def test_noPassword(self):
        resp = self.client.post("/", {"email": "kravtso5@uwm.edu", "password": ""})
        self.assertEqual(resp.status_code, 200, "Login should have failed, no password")
    
