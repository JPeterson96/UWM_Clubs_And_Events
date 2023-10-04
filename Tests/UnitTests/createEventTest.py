from django.test import TestCase
from classes.event_util import Event_Util as event_util

class TestCreateEvent(TestCase):

    def test_createEvent(self):
        self.made = event_util.create_event(self, name = "Club meeting", org = "CS Smart Club", location = "location", date = "date", 
                                time = "time", description = "description", background_image = None, type = "type")
        self.assertEqual(self.made, True)

        self.event = event_util.get_event("Club meeting") #create event id to search for events?
        self.assertEqual(self.event.name, "Club meeting")
        self.assertEqual(self.event.org, "Cs Smart Club")
        self.assertEqual(self.event.location, "location")
        self.assertEqual(self.event.date, "date")
        self.assertEqual(self.event.time, "time")
        self.assertEqual(self.event.description, "description")
        self.assertEqual(self.event.type, "type")

class TestInvalidInput(TestCase):

    def test_emptyName(self):
        self.made = event_util.create_event(name = "", org = "CS Smart Club", location = "location", date = "date", 
                                time = "time", description = "description", background_image = None, type = "type")
        self.assertEqual(self.made, False)

    def test_emptyOrg(self):
        self.made = event_util.create_event(name = "Club meeting", org = "", location = "location", date = "date", 
                                time = "time", description = "description", background_image = None, type = "type")        
        self.assertEqual(self.made, False)
    
    def test_emptyLocation(self):
        self.made = event_util.create_event(name = "Club meeting", org = "CS Smart Club", location = "", date = "date", 
                                time = "time", description = "description", background_image = None, type = "type")
        self.assertEqual(self.made, False)  

    def test_emptyDate(self):
        self.made = event_util.create_event(name = "Club meeting", org = "CS Smart Club", location = "location", date = "", 
                                time = "time", description = "description", background_image = None, type = "type")
        self.assertEqual(self.made, False)

    def test_emptyTime(self):
        self.made = event_util.create_event(name = "Club meeting", org = "CS Smart Club", location = "location", date = "date", 
                                time = "", description = "description", background_image = None, type = "type")
        self.assertEqual(self.made, False)

    def test_emptyDescription(self):
        self.made = event_util.create_event(name = "Club meeting", org = "CS Smart Club", location = "location", date = "date", 
                                time = "time", description = "", background_image = None, type = "type")
        self.assertEqual(self.made, False)

    def test_emptyType(self):
        self.made = event_util.create_event(name = "Club meeting", org = "CS Smart Club", location = "location", date = "date", 
                                time = "time", description = "description", background_image = None, type = "")
        self.assertEqual(self.made, False)