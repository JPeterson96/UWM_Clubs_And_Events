from django.test import TestCase
from UWM_Clubs_and_Events.models import Event
from classes.event_util import Event_Util
import datetime

#class TestGetEvent(TestCase):
#
#    def test_getEventValid(self):
#        self.event = Event(id = 1)
#        self.event.save()
#        self.assertEqual(Event_Util.getEvent(1), self.event)

#class TestGetEventInvalid(TestCase):
#
#    def test_getEventInvalid(self):
#        self.assertEqual(Event_Util.get_event(1), None, "Event should not have been found")

class TestgetAllEvents(TestCase):

    def test_getAllEvents(self):
        self.event = Event(time = datetime.datetime.now())
        self.event.save()
        self.assertTrue(self.event in Event_Util.get_all_events())

class TestgetOrgEvents(TestCase):
    def test_getOrgEvents(self):
        self.event = Event(organization = "CS Smart Club", time = datetime.datetime(2020, 1, 1, 0, 0, 0))
        self.event.save()
        self.assertTrue(self.event in Event_Util.get_org_events("CS Smart Club"))

class TestgetOrgEventsInvalid(TestCase):
     
    def test_getOrgEventsInvalid(self):
        self.assertFalse(Event_Util.get_org_events("NonExistent").exists(), "No orgs should have been found")

class TestgetEventByName(TestCase):
         
    def test_getEventByName(self):
        self.event = Event(name = "Club meeting", time = datetime.datetime(2020, 1, 1, 0, 0, 0))
        self.event.save()
        self.assertTrue(self.event in Event_Util.get_event_by_name("Club meeting"))

class TestgetEventByNameInvalid(TestCase):

    def test_getEventByNameInvalid(self):
        self.assertFalse(Event_Util.get_event_by_name("NonExistent").exists(), "No events should have been found")
