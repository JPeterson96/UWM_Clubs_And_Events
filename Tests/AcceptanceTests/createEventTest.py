from django.test import TestCase
from django.test import Client
from UWM_Clubs_and_Events.models import Event
from classes.event_util import Event_Util
from UWM_Clubs_and_Events.models import User
from UWM_Clubs_and_Events.models import Organization
from classes.user_util import User_Util as user_util
import datetime

class TestCreateValidEvent(TestCase):
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
        
    def test_createEvent(self):
        self.time = datetime.datetime(year=2020, month=1, day=1, hour=0, minute=0, second=0, tzinfo = datetime.timezone.utc)
        self.resp = self.client.post("/createEvent/", {"name": "Test Event", "org": "CS Smart Club", 
                                                       "loc_addr": "1234 Test St.", 
                                                       "loc_city": "Milwaukee,WI", "loc_zip": "53211", 
                                                       "time-happening": self.time, 
                                                       "description": "Test Event", 
                                                       "photo": "static/event_photos/default.jpeg"})
        self.assertEqual(self.resp.status_code, 200)
        self.assertEquals(self.resp.context["message"], "Event created successfully")
        self.assertIsNotNone(Event_Util.get_event(1))

class TestCreateInvalidEvent(TestCase):
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

    def test_createEventInvalidName(self):
        self.time = datetime.datetime(year=2020, month=1, day=1, hour=0, minute=0, second=0, tzinfo = datetime.timezone.utc)
        self.resp = self.client.post("/createEvent/", {"name": "", "org": "CS Smart Club", 
                                                       "loc_addr": "1234 Test St.", 
                                                       "loc_city": "Milwaukee,WI", "loc_zip": "53211", 
                                                       "time-happening": self.time, 
                                                       "description": "Test Event", 
                                                       "photo": "static/event_photos/default.jpeg"})
        self.assertEqual(self.resp.status_code, 200)
        self.assertEquals(self.resp.context["message"], "Invalid event name")
        self.assertIsNone(Event_Util.get_event(1))

    def test_createEventInvalidOrg(self):
        self.time = datetime.datetime(year=2020, month=1, day=1, hour=0, minute=0, second=0, tzinfo = datetime.timezone.utc)
        self.resp = self.client.post("/createEvent/", {"name": "Test Event", "org": "", 
                                                       "loc_addr": "1234 Test St.", 
                                                       "loc_city": "Milwaukee,WI", "loc_zip": "53211", 
                                                       "time-happening": self.time, 
                                                       "description": "Test Event", 
                                                       "photo": "static/event_photos/default.jpeg"})
        self.assertEqual(self.resp.status_code, 200)
        self.assertEquals(self.resp.context["message"], "Selected organization does not exist")
        self.assertIsNone(Event_Util.get_event(1))

    def test_createEventInvalidLocAddr(self):
        self.time = datetime.datetime(year=2020, month=1, day=1, hour=0, minute=0, second=0, tzinfo = datetime.timezone.utc)
        self.resp = self.client.post("/createEvent/", {"name": "Test Event", "org": "CS Smart Club", 
                                                       "loc_addr": "", 
                                                       "loc_city": "Milwaukee,WI", "loc_zip": "53211", 
                                                       "time-happening": self.time, 
                                                       "description": "Test Event", 
                                                       "photo": "static/event_photos/default.jpeg"})
        self.assertEqual(self.resp.status_code, 200)
        self.assertEquals(self.resp.context["message"], "Invalid location address")
        self.assertIsNone(Event_Util.get_event(1))


    def test_createEventInvalidLocCity(self):
        self.time = datetime.datetime(year=2020, month=1, day=1, hour=0, minute=0, second=0, tzinfo = datetime.timezone.utc)
        self.resp = self.client.post("/createEvent/", {"name": "Test Event", "org": "CS Smart Club", 
                                                       "loc_addr": "1234 Test St.", 
                                                       "loc_city": "", "loc_zip": "53211", 
                                                       "time-happening": self.time, 
                                                       "description": "Test Event", 
                                                       "photo": "static/event_photos/default.jpeg"})
        self.assertEqual(self.resp.status_code, 200)
        self.assertIsNone(Event_Util.get_event(1))

    def test_createEventInvalidLocZip(self):
        self.time = datetime.datetime(year=2020, month=1, day=1, hour=0, minute=0, second=0, tzinfo = datetime.timezone.utc)
        self.resp = self.client.post("/createEvent/", {"name": "Test Event", "org": "CS Smart Club", 
                                                       "loc_addr": "1234 Test St.", 
                                                       "loc_city": "Milwaukee,WI", "loc_zip": "", 
                                                       "time-happening": self.time, 
                                                       "description": "Test Event", 
                                                       "photo": "static/event_photos/default.jpeg"})
        self.assertEqual(self.resp.status_code, 200)
        self.assertEquals(self.resp.context["message"], "Invalid location zip")
        self.assertIsNone(Event_Util.get_event(1))

    def test_createEventInvalidDescription(self):
        self.time = datetime.datetime(year=2020, month=1, day=1, hour=0, minute=0, second=0, tzinfo = datetime.timezone.utc)
        self.resp = self.client.post("/createEvent/", {"name": "Test Event", "org": "CS Smart Club", 
                                                       "loc_addr": "1234 Test St.", 
                                                       "loc_city": "Milwaukee,WI", "loc_zip": "53211", 
                                                       "time-happening": self.time, 
                                                       "description": "", 
                                                       "photo": "static/event_photos/default.jpeg"})
        self.assertEqual(self.resp.status_code, 200)
        self.assertEquals(self.resp.context["message"], "Invalid description")
        self.assertIsNone(Event_Util.get_event(1))

class TestCreateEventNotLoggedIn(TestCase):
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