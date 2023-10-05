from django.test import TestCase
from classes.event_util import Event_Util as event_util
import datetime

class TestCreateEvent(TestCase):

    def test_createEvent(self):
        self.time = datetime.datetime(year=2020, month=1, day=1, hour=0, minute=0, second=0, tzinfo = datetime.timezone.utc)
        self.made = event_util.create_event("Club meeting", "CS Smart Club", "location", 
                                            self.time , "description")
        self.assertEqual(self.made, True, "Event should have been created, returned false")

        self.event = event_util.get_org_events("CS Smart Club").first()
        self.assertEqual(self.event.name, "Club meeting", "Name should be Club meeting")
        self.assertEqual(self.event.organization, "CS Smart Club", "Organization should be CS Smart Club")
        self.assertEqual(self.event.location, "location", "Location should be location")
        self.assertEqual(self.event.time, self.time, "Time should be 2020-01-01 00:00:00")
        self.assertEqual(self.event.description, "description", "Description should be description")

class TestInvalidInput(TestCase):

    def setUp(self):
        self.time = datetime.datetime(year=2020, month=1, day=1, hour=0, minute=0, second=0, tzinfo = datetime.timezone.utc)

    def test_emptyName(self):
        with self.assertRaises(TypeError, msg="Missing Name"):
            self.test = event_util.create_event(org = "CS Smart Club", location = "location", 
                                                time = self.time , description = "description")
            
    def test_emptyOrg(self):
        with self.assertRaises(TypeError, msg="Missing Organization"):
            self.test = event_util.create_event(name = "Club meeting", location = "location", 
                                                time = self.time , description = "description")
    
    def test_emptyLocation(self):
        with self.assertRaises(TypeError, msg="Missing Location"):
            self.test = event_util.create_event(name = "Club meeting", org  ="CS Smart Club", 
                                                time = self.time , description = "description")
    
    def test_emptyTime(self):
        with self.assertRaises(TypeError, msg="Missing Time"):
            self.test = event_util.create_event(name = "Club meeting", org = "CS Smart Club", location = "location", 
                                                 description = "description")
            
    def test_emptyDescription(self):
        with self.assertRaises(TypeError, msg="Missing Description"):
            self.test = event_util.create_event(name = "Club meeting", org = "CS Smart Club", location = "location", 
                                                time = self.time)

