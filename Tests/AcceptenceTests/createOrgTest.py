from django.test import TestCase
from django.test import Client
from UWM_Clubs_and_Events.models import Organization as Org

class TestCreateValidOrg(TestCase):
    def setUp(self):
        self.client = Client()

    def test_createOrg(self):
        self.resp = self.client.post("/createorg/", {"name": "CS Smart Club", "point of contact": "poc",
                                                     "description": "description"}, follow=True)

        self.assertEqual("Success: New Org has been created", self.resp.context["msg"],
                         "Failed creation. One or more fields invalid")

class TestCreateInvalid(TestCase):
    def setUp(self):
        self.client = Client()

    def test_emptyFields(self):
        self.resp = self.client.post("/createorg/", {"name": "", "point of contact": "",
                                                     "description": ""}, follow=True)
        self.assertEqual("Error: One or more fields invalid", self.resp.context["msg"],
                         "Org created with one or more fields empty")

    def test_blankField(self):
        self.resp = self.client.post("/createorg/", {"name": " ", "point of contact": " ",
                                                     "description": " "}, follow=True)
        self.assertEqual("Error: One or more fields invalid", self.resp.context["msg"],
                         "Org created with one or more fields blank")

    def test_duplicateOrg(self):
        self.org = Org(name = "CS Smart Club", point_of_contact = "poc", description = "description")
        self.org.save()
        self.resp = self.client.post("/createorg/", {"name": "CS Smart Club", "point of contact": "poc",
                                                     "description": "description"}, follow=True)
        self.assertEqual("Error: One or more fields invalid", self.resp.context["msg"],
                         "Duplicate org created")