from django.test import TestCase
from django.test import Client
from UWM_Clubs_and_Events.models import Event

class TestCreateValidEvent(TestCase):
    def setUp(self):
        self.client = Client()

    def test_createOrg(self):
        self.resp = self.client.post("/createevent/", {"name": "Club meeting", "org": "CS Smart Club", 
                                     "location": "EMS", "date": "2024/01/01", "time": "4:30:00",
                                     "description": }, follow=True)
        self.assertEqual("Success: New Event has been created", self.resp.context["msg"],
                         "Failed creation. One or more fields invalid")

class TestCreateInvalid(TestCase):
    def setUp(self):
        self.client = Client()

    def test_emptyFields(self):
        self.resp = self.client.post("/createevent/", {"name": "", "org": "",
                                     "location": "", "date": "", "time": "",
                                     "description": ""}, follow=True)
        self.assertEqual("Error: One or more fields invalid", self.resp.context["msg"],
                         "Event created with one or more fields empty")

    def test_blankField(self):
        self.resp = self.client.post("/createevent/", {"name": " ", "org": " ",
                                     "location": " ", "date": " ", "time": " ",
                                     "description": " "}, follow=True)
        self.assertEqual("Error: One or more fields invalid", self.resp.context["msg"],
                         "Event created with one or more fields blank")

    def test_duplicateEvent(self):
        self.event = Event(name = "Club meeting", org = "CS Smart Club", location = "EMS", 
                           date = "2024/01/01", time = "4:30:00", description = "description")
        self.event.save()
        self.resp = self.client.post("/createevent/", {"name": "Club meeting", "org": "CS Smart Club", 
                                     "location": "EMS", "date": "2024/01/01", "time": "4:30:00",
                                     "description": "description"}, follow=True)
        self.assertEqual("Error: One or more fields invalid", self.resp.context["msg"],
                         "Duplicate event created")