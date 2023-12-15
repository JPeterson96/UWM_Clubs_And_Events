from django.test import TestCase
from django.test import Client
from UWM_Clubs_and_Events.models import Event
from classes.event_util import Event_Util
from UWM_Clubs_and_Events.models import User
from UWM_Clubs_and_Events.models import Organization
from classes.user_util import User_Util as user_util
import datetime

class TestValidEditEvent(TestCase):
    def setUp(self):
        self.client = Client()
        self.time = datetime.datetime(year=2020, month=1, day=1, hour=0, minute=0, second=0, tzinfo = datetime.timezone.utc)
        user_util.create_user(name = "Ilya", email = "kravtso5@uwm.edu", password = "123", role = 3, 
                              startdate = self.time, graddate = self.time)
        self.user = user_util.get_user("kravtso5@uwm.edu")
        self.client.post("/", {"email": "kravtso5@uwm.edu", "password": "123"})
        self.client.post("/createOrganization/", {"email": "cssmartclub@uwm.edu", "password": "password", 
                                                    "name": "CS Smart Club", "point_of_contact": "1",
                                                    "member_count": "1", "description": "description"})
        self.org = Organization.objects.get(name="CS Smart Club")
        self.resp = self.client.post("/createEvent/", {"name": "Test Event", "org": "CS Smart Club", 
                                                       "loc_addr": "1234 Test St.", 
                                                       "loc_city": "Milwaukee,WI", "loc_zip": "53211", 
                                                       "time-happening": self.time, 
                                                       "description": "Test Event", 
                                                       "photo": "static/event_photos/default.jpeg"})
        self.event = Event.objects.get(name="Test Event")

    def test_editEvent(self):
        self.resp = self.client.post("/editEvent/1/", {"name": "Test Event 2", 
                                                       "loc_addr": "1235 Test St.", 
                                                       "loc_city": "Greenbay,WI", "loc_zip": "54299", 
                                                       "time_happening": self.time,
                                                       "description": "Test Event 2"})
        self.assertEqual(self.resp.status_code, 200)
        self.event = Event.objects.get(name="Test Event 2")
        self.assertEqual(self.event.name, "Test Event 2")
        self.assertEqual(self.event.loc_addr, "1235 Test St.")
        self.assertEqual(self.event.loc_city, "Greenbay")
        self.assertEqual(self.event.loc_zip, "54299")
        self.assertEqual(self.event.time_happening, self.time)
        self.assertEqual(self.event.description, "Test Event 2")

class TestInValidEditEvent(TestCase):
    def setUp(self):
        self.client = Client()
        self.time = datetime.datetime(year=2020, month=1, day=1, hour=0, minute=0, second=0, tzinfo = datetime.timezone.utc)
        user_util.create_user(name = "Ilya", email = "kravtso5@uwm.edu", password = "123", role = 3, 
                              startdate = self.time, graddate = self.time)
        self.user = user_util.get_user("kravtso5@uwm.edu")
        self.client.post("/", {"email": "kravtso5@uwm.edu", "password": "123"})
        self.client.post("/createOrganization/", {"email": "cssmartclub@uwm.edu", "password": "password", 
                                                    "name": "CS Smart Club", "point_of_contact": "1",
                                                    "member_count": "1", "description": "description"})
        self.org = Organization.objects.get(name="CS Smart Club")
        self.resp = self.client.post("/createEvent/", {"name": "Test Event", "org": "CS Smart Club", 
                                                       "loc_addr": "1234 Test St.", 
                                                       "loc_city": "Milwaukee,WI", "loc_zip": "53211", 
                                                       "time-happening": self.time, 
                                                       "description": "Test Event", 
                                                       "photo": "static/event_photos/default.jpeg"})
        self.event = Event.objects.get(name="Test Event")

    def test_editEventNoName(self):
        self.resp = self.client.post("/editEvent/1/", {"name": "", 
                                                       "loc_addr": "1235 Test St.", 
                                                       "loc_city": "Greenbay,WI", "loc_zip": "54299", 
                                                       "time_happening": self.time,
                                                       "description": "Test Event 2"})
        self.assertEqual(self.resp.status_code, 200)
        self.assertEqual(self.event.name, "Test Event")

    def test_editEventNoAddress(self):
        self.resp = self.client.post("/editEvent/1/", {"name": "Test Event 2", 
                                                       "loc_addr": "", 
                                                       "loc_city": "Greenbay,WI", "loc_zip": "54299", 
                                                       "time_happening": self.time,
                                                       "description": "Test Event 2"})
        self.assertEqual(self.resp.status_code, 200)
        self.assertEqual(self.event.loc_addr, "1234 Test St.")

    def test_editEventNoCity(self):
        self.resp = self.client.post("/editEvent/1/", {"name": "Test Event 2", 
                                                       "loc_addr": "1235 Test St.", 
                                                       "loc_city": "", "loc_zip": "54299", 
                                                       "time_happening": self.time,
                                                       "description": "Test Event 2"})
        self.assertEqual(self.resp.status_code, 200)
        self.assertEqual(self.event.loc_city, "Milwaukee")

    def test_editEventNoZip(self):
        self.resp = self.client.post("/editEvent/1/", {"name": "Test Event 2", 
                                                       "loc_addr": "1235 Test St.", 
                                                       "loc_city": "Greenbay,WI", "loc_zip": "", 
                                                       "time_happening": self.time,
                                                       "description": "Test Event 2"})
        self.assertEqual(self.resp.status_code, 200)
        self.assertEqual(self.event.loc_zip, "53211")

    def test_editEventNoDescription(self):
        self.resp = self.client.post("/editEvent/1/", {"name": "Test Event 2", 
                                                       "loc_addr": "1235 Test St.", 
                                                       "loc_city": "Greenbay,WI", "loc_zip": "54299", 
                                                       "time_happening": self.time,
                                                       "description": ""})
        self.assertEqual(self.resp.status_code, 200)
        self.assertEqual(self.event.description, "Test Event")
