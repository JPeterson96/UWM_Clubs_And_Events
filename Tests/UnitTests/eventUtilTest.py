from django.test import TestCase
from UWM_Clubs_and_Events.models import Event
from classes.event_util import Event_Util
from UWM_Clubs_and_Events.models import User
from UWM_Clubs_and_Events.models import Organization
import datetime

class TestGetEvent(TestCase):

    def setUp(self):
        self.user = User.objects.create(name="TestOrg", email="testOrg@uwm.edu", password="123", role=3)
        self.orgUser = User.objects.create(email="csssmartclub@uwm.edu", password="123", name="CS Smart Club", role=2) 
        self.org = Organization.objects.create(user=self.orgUser, name="TestOrg", point_of_contact="kravtso5@uwm.edu", 
                                               membersCount=1, description="Test Org")
        self.event = Event.objects.create(name="Test Event", organization=self.org, loc_addr="1234 Test St.", loc_state="WI", 
                             loc_city="Milwaukee", loc_zip="53211", time_happening=datetime.datetime.now(), 
                             description="Test Event", time_published=datetime.datetime.now(), 
                             image="static/event_photos/default.jpeg")
        
    def test_getEvent(self):
        self.event2 = Event_Util.get_event(1)
        self.assertEqual(self.event, self.event2, "Event should match")
        self.assertEqual(self.event2.name, "Test Event", "Event name should match")
        self.assertEqual(self.event2.organization, self.org, "Organization should match")
        self.assertEqual(self.event2.loc_addr, "1234 Test St.", "Address should match")
        self.assertEqual(self.event2.loc_state, "WI", "State should match")
        self.assertEqual(self.event2.loc_city, "Milwaukee", "City should match")
        self.assertEqual(self.event2.loc_zip, "53211", "Zip should match")
        self.assertEqual(self.event2.description, "Test Event", "Description should match")
        self.assertEqual(self.event2.image, "static/event_photos/default.jpeg", "Image should match")

    def test_getEventInvalid(self):
        self.event2 = Event_Util.get_event(2)
        self.assertEqual(self.event2, None, "Event should be None")

class editEvent(TestCase):
    def setUp(self):
        self.user = User.objects.create(name="TestOrg", email="testOrg@uwm.edu", password="123", role=3)
        self.orgUser = User.objects.create(email="csssmartclub@uwm.edu", password="123", name="CS Smart Club", role=2) 
        self.org = Organization.objects.create(user=self.orgUser, name="TestOrg", point_of_contact="kravtso5@uwm.edu", 
                                               membersCount=1, description="Test Org")
        self.event = Event.objects.create(name="Test Event", organization=self.org, loc_addr="1234 Test St.", loc_state="WI", 
                             loc_city="Milwaukee", loc_zip="53211", time_happening=datetime.datetime.now(), 
                             description="Test Event", time_published=datetime.datetime.now(), 
                             image="static/event_photos/default.jpeg")
        
    def test_editEventEmptyName(self):
        with self.assertRaises(ValueError, msg="Name should not be empty"):
            Event_Util.edit_event(1, "", "1234 Test St.", "WI", "Milwaukee", "53211", datetime.datetime.now(), 
                                  "Test Event", datetime.datetime.now(), "static/event_photos/default.jpeg")
        
    def test_editEventEmptyAddress(self):
        with self.assertRaises(ValueError, msg="Address should not be empty"):
            Event_Util.edit_event(1, "Test Event", "", "WI", "Milwaukee", "53211", datetime.datetime.now(), 
                                  "Test Event", datetime.datetime.now(), "static/event_photos/default.jpeg")
            
    def test_editEventEmptyState(self):
        with self.assertRaises(ValueError, msg="State should not be empty"):
            Event_Util.edit_event(1, "Test Event", "1234 Test St.", "", "Milwaukee", "53211", datetime.datetime.now(), 
                                  "Test Event", datetime.datetime.now(), "static/event_photos/default.jpeg")
            
    def test_editEventEmptyCity(self):
        with self.assertRaises(ValueError, msg="City should not be empty"):
            Event_Util.edit_event(1, "Test Event", "1234 Test St.", "WI", "", "53211", datetime.datetime.now(), 
                                  "Test Event", datetime.datetime.now(), "static/event_photos/default.jpeg")
            
    def test_editEventEmptyZip(self):
        with self.assertRaises(ValueError, msg="Zip should not be empty"):
            Event_Util.edit_event(1, "Test Event", "1234 Test St.", "WI", "Milwaukee", "", datetime.datetime.now(), 
                                  "Test Event", datetime.datetime.now(), "static/event_photos/default.jpeg")
            
    def test_editEventEmptyDescription(self):
        with self.assertRaises(ValueError, msg="Description should not be empty"):
            Event_Util.edit_event(1, "Test Event", "1234 Test St.", "WI", "Milwaukee", "53211", datetime.datetime.now(), 
                                  "", datetime.datetime.now(), "static/event_photos/default.jpeg")
            
    def test_editEventEmptyImage(self):
        with self.assertRaises(ValueError, msg="Image should not be empty"):
            Event_Util.edit_event(1, "Test Event", "1234 Test St.", "WI", "Milwaukee", "53211", datetime.datetime.now(), 
                                  "Test Event", datetime.datetime.now(), "")
                                        