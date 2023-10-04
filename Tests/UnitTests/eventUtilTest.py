from django.test import TestCase
from UWM_Clubs_and_Events.models import Event
from classes.event_util import Event_Util

class TestGetEvent(TestCase):

    def test_getEventValid(self):
        self.event = Event(name = "Club meeting", org = "CS Smart Club", location = "EMS", 
                           date = "2024/01/01", time = "4:30:00", description = "description", id = 1)
        self.event.save()
        self.assertEqual(Event_Util.getEvent(1), self.event)

class TestGetEventInvalid(TestCase):

    def test_getEventInvalid(self):
        self.assertEqual(Event_Util.getEvent(1), None)

class TestgetAllEvents(TestCase):

    def test_getAllEvents(self):
        self.event = Event(name = "Club meeting", org = "CS Smart Club", location = "EMS", 
                        date = "2024/01/01", time = "4:30:00", description = "description")
        self.event.save()
        self.assertTrue(self.event in Event_Util.getAllEvents())

class TestgetAllEventsInvalid(TestCase):
     
    def test_getAllEventsInvalid(self):
        self.event = Event(name = "Club meeting", org = "CS Smart Club", location = "EMS", 
                        date = "2024/01/01", time = "4:30:00", description = "description")
        self.event.save()
        self.assertFalse(self.event not in Event_Util.getAllEvents())

class TestgetOrgEvents(TestCase):

    def test_getOrgEvents(self):
        self.event = Event(name = "Club meeting", org = "CS Smart Club", location = "EMS", 
                        date = "2024/01/01", time = "4:30:00", description = "description")
        self.event.save()
        self.assertTrue(self.event in Event_Util.getOrgEvents("CS Smart Club"))

class TestgetOrgEventsInvalid(TestCase):
     
    def test_getOrgEventsInvalid(self):
        self.event = Event(name = "Club meeting", org = "CS Smart Club", location = "EMS", 
                        date = "2024/01/01", time = "4:30:00", description = "description")
        self.event.save()
        self.assertFalse(self.event not in Event_Util.getOrgEvents("CS Smart Club"))

class TestgetEventByName(TestCase):
         
    def test_getEventByName(self):
        self.event = Event(name = "Club meeting", org = "CS Smart Club", location = "EMS", 
                        date = "2024/01/01", time = "4:30:00", description = "description")
        self.event.save()
        self.assertTrue(self.event in Event_Util.getEventByName("Club meeting"))

class TestgetEventByNameInvalid(TestCase):

    def test_getEventByNameInvalid(self):
        self.event = Event(name = "Club meeting", org = "CS Smart Club", location = "EMS", 
                            date = "2024/01/01", time = "4:30:00", description = "description")
        self.event.save()
        self.assertFalse(self.event not in Event_Util.getEventByName("Club meeting"))
