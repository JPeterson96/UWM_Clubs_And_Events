from django.test import TestCase
from django.test import Client
from UWM_Clubs_and_Events.models import User

class SuccessfulLogout(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User(name = "Ilya", email = "kravtso5@uwm.edu", password = "123", role = 0)
        self.user.save()
        self.client.post("/", {"email": "kravtso5@uwm.edu", "password": "123"})

    def test_successfulLogout(self):
        response = self.client.get("/login/")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")