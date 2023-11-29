from django.test import TestCase
from classes.event_util import Event_Util as event_util
from classes.organization_util import Organization_Util as org_util
from classes.user_util import User_Util as user_util
import datetime

class TestCreateEvent(TestCase):

    def test_createEvent(self):
        self.time = datetime.datetime(year=2020, month=1, day=1, hour=0, minute=0, second=0, tzinfo = datetime.timezone.utc)
        user_util.create_user(name = "Ilya", email = "kravtso5@uwm.edu", password = "123", role = 0, 
                                          startdate = self.time, graddate = self.time)
        org_util.create_organization("CS Smart Club", "cssclub@uwm.edu", "123", 2, "kravtso5@uwm.edu", 1, "description")
        self.made = event_util.create_event("Club meeting", org_util.get_org_by_name("CS Smart Club"), "2200 E Kenwood Blvd", "Milwaukee", "WI", "53211", 
                                            self.time, "description")
        self.assertEqual(self.made, True, "Event should have been created, returned false")

        self.event = event_util.get_org_events("CS Smart Club").first()
        self.assertEqual(self.event.name, "Club meeting", "Name should be Club meeting")
        self.assertEqual(self.event.organization.name, "CS Smart Club", "Organization should be CS Smart Club")
        self.assertEqual(self.event.loc_addr, "2200 E Kenwood Blvd", "Adress should be 2200 E Kenwood Blvd")
        self.assertEqual(self.event.loc_city, "Milwaukee", "City should be Milwaukee")
        self.assertEqual(self.event.loc_state, "WI", "State should be WI")
        self.assertEqual(self.event.loc_zip, "53211", "Zip should be 53211")
        self.assertEqual(self.event.time_happening, self.time, "Time should be 2020-01-01 00:00:00")
        self.assertEqual(self.event.description, "description", "Description should be description")

class TestInvalidInput(TestCase):

    def setUp(self):
        self.time = datetime.datetime(year=2020, month=1, day=1, hour=0, minute=0, second=0, tzinfo = datetime.timezone.utc)
        user_util.create_user(name = "Ilya", email = "kravtso5@uwm.edu", password = "123", role = 0, 
                                     startdate = self.time, graddate = self.time)
        self.user= user_util.get_user("kravtso5@uwm.edu")
        org_util.create_organization("CS Smart Club", "cssclub@uwm.edu", "123", 2, "kravtso5@uwm.edu", 1, "description")
        self.org = org_util.get_org_by_name("CS Smart Club")

    def test_emptyName(self):
        with self.assertRaises(ValueError, msg="Missing Name"):
            self.test = event_util.create_event(name = "", org = self.org, loc_addr = "2200 E Kenwood Blvd", 
                                                loc_city = "Milwaukee", loc_state = "WI", loc_zip = "53211", 
                                                time = self.time, description = "description")
            
    def test_emptyOrg(self):
        with self.assertRaises(ValueError, msg="Missing Organization"):
            self.test = event_util.create_event(name = "Club meeting", org = None, loc_addr = "2200 E Kenwood Blvd", 
                                                loc_city = "Milwaukee", loc_state = "WI", loc_zip = "53211", 
                                                time = self.time, description = "description")
    
    def test_emptyAdress(self):
        with self.assertRaises(ValueError, msg="Missing Address"):
            self.test = event_util.create_event(name = "Club meeting", org  = self.org, loc_addr = "", 
                                                loc_city = "Milwaukee", loc_state = "WI", loc_zip = "53211", 
                                                time = self.time, description = "description")
            
    def test_emptyCity(self):
        with self.assertRaises(ValueError, msg="Missing City"):
            self.test = event_util.create_event(name = "Club meeting", org = self.org, loc_addr = "2200 E Kenwood Blvd", 
                                                loc_city = "", loc_state = "WI", loc_zip = "53211", 
                                                time = self.time, description = "description")
            
    def test_emptyState(self):
        with self.assertRaises(ValueError, msg="Missing State"):
            self.test = event_util.create_event(name = "Club meeting", org = self.org, loc_addr = "2200 E Kenwood Blvd", 
                                                loc_city = "Milwaukee", loc_state = "", loc_zip = "53211", 
                                                time = self.time, description = "description")
            
    def test_emptyZip(self):
        with self.assertRaises(ValueError, msg="Missing Zip"):
            self.test = event_util.create_event(name = "Club meeting", org = self.org, loc_addr = "2200 E Kenwood Blvd", 
                                                loc_city = "Milwaukee", loc_state = "WI", loc_zip = "", 
                                                time = self.time, description = "description")
    
    def test_emptyTime(self):
        with self.assertRaises(ValueError, msg="Missing Time"):
            self.test = event_util.create_event(name = "Club meeting", org = self.org, loc_addr = "2200 E Kenwood Blvd", 
                                                loc_city = "Milwaukee", loc_state = "WI", loc_zip = "53211", 
                                                time = None, description = "description")
            
    def test_emptyDescription(self):
        with self.assertRaises(ValueError, msg="Missing Description"):
            self.test = event_util.create_event(name = "Club meeting", org = self.org, loc_addr = "2200 E Kenwood Blvd", 
                                                loc_city = "Milwaukee", loc_state = "WI", loc_zip = "53211", 
                                                time = self.time, description = "")

