from django.test import TestCase
from django.test import Client
from classes.user_util import User_Util as user_util
from classes.organization_util import Organization_Util as org_util
import datetime

class TestCreateValidOrg(TestCase):
    def setUp(self):
        self.client = Client()
        self.time = datetime.datetime(year=2020, month=1, day=1, hour=0, minute=0, second=0, tzinfo = datetime.timezone.utc)
        user_util.create_user(name = "Ilya", email = "kravtso5@uwm.edu", password = "123", role = 3, 
                              startdate = self.time, graddate = self.time)
        self.user = user_util.get_user("kravtso5@uwm.edu")
        self.client.post("/", {"email": "kravtso5@uwm.edu", "password": "123"})

    def test_createOrg(self):
        self.resp = self.client.post("/createOrganization/", {"email": "cssmartclub@uwm.edu", "password": "password", 
                                                     "name": "CS Smart Club", "point_of_contact": "1",
                                                     "member_count": "1", "description": "description"})
        self.assertEqual(self.resp.status_code, 200)
        self.assertEquals(self.resp.context["success_message"], "Organization Successfully created")
        self.assertIsNotNone(org_util.get_org_by_name("CS Smart Club"))

class TestCreateInvalidOrg(TestCase):
    def setUp(self):
        self.client = Client()
        self.time = datetime.datetime(year=2020, month=1, day=1, hour=0, minute=0, second=0, tzinfo = datetime.timezone.utc)
        user_util.create_user(name = "Ilya", email = "kravtso5@uwm.edu", password = "123", role = 3, 
                              startdate = self.time, graddate = self.time)
        self.client.post("/", {"email": "kravtso5@uwm.edu", "password": "123"})

        
    def test_createOrgEmptyName(self):
        self.resp = self.client.post("/createOrganization/", {"email": "cssmartclub@uwm.edu", "password": "password", 
                                                     "name": "", "point_of_contact": "1",
                                                        "member_count": "1", "description": "description"})
        self.assertEqual(self.resp.status_code, 200)
        self.assertIsNone(org_util.get_org_by_name("CS Smart Club"))

    def test_createOrgEmptyEmail(self):
        self.resp = self.client.post("/createOrganization/", {"email": "", "password": "password", 
                                                     "name": "CS Smart Club", "point_of_contact": "1",
                                                        "member_count": "1", "description": "description"})
        self.assertEqual(self.resp.status_code, 200)
        self.assertIsNone(org_util.get_org_by_name("CS Smart Club"))

    def test_createOrgEmptyPassword(self):
        self.resp = self.client.post("/createOrganization/", {"email": "cssmartclub@uwm.edu", "password": "", 
                                                     "name": "CS Smart Club", "point_of_contact": "1",
                                                        "member_count": "1", "description": "description"})
        self.assertEqual(self.resp.status_code, 200)
        self.assertIsNone(org_util.get_org_by_name("CS Smart Club"))

    def test_createOrgEmptyPOC(self):
        self.resp = self.client.post("/createOrganization/", {"email": "cssmartclub@uwm.edu", "password": "password", 
                                                     "name": "CS Smart Club", "point_of_contact": "-1",
                                                        "member_count": "1", "description": "description"})
        self.assertEqual(self.resp.status_code, 200)
        self.assertEquals(self.resp.context["error_message"], "User does not exist")
        self.assertIsNone(org_util.get_org_by_name("CS Smart Club"))

    def test_createOrgInvalidPOC(self):
        self.resp = self.client.post("/createOrganization/", {"email": "cssmartclub@uwm.edu", "password": "password", 
                                                     "name": "CS Smart Club", "point_of_contact": "-1",
                                                        "member_count": "1", "description": "description"})
        self.assertEqual(self.resp.status_code, 200)
        self.assertEquals(self.resp.context["error_message"], "User does not exist")
        self.assertIsNone(org_util.get_org_by_name("CS Smart Club"))

    def test_createOrgInvalidMembers(self):
        self.resp = self.client.post("/createOrganization/", {"email": "cssmartclub@uwm.edu", "password": "password", 
                                                     "name": "CS Smart Club", "point_of_contact": "1",
                                                        "member_count": "-1", "description": "description"})
        self.assertEqual(self.resp.status_code, 200)
        self.assertIsNone(org_util.get_org_by_name("CS Smart Club"))

    def test_createOrgInvalidDescription(self):
        self.resp = self.client.post("/createOrganization/", {"email": "cssmartclub@uwm.edu", "password": "password", 
                                                     "name": "CS Smart Club", "point_of_contact": "1",
                                                        "member_count": "1", "description": ""})
        self.assertEqual(self.resp.status_code, 200)
        self.assertIsNone(org_util.get_org_by_name("CS Smart Club"))

    def test_createOrgInvalidEmail(self):
        self.resp = self.client.post("/createOrganization/", {"email": "cssmartclub", "password": "password", 
                                                     "name": "CS Smart Club", "point_of_contact": "1",
                                                        "member_count": "1", "description": "description"})
        self.assertEqual(self.resp.status_code, 200)
        self.assertIsNone(org_util.get_org_by_name("CS Smart Club"))

class testCreateOrgNotLoggedIn(TestCase):
    def setUp(self):
        self.client = Client()
        self.time = datetime.datetime(year=2020, month=1, day=1, hour=0, minute=0, second=0, tzinfo = datetime.timezone.utc)
        user_util.create_user(name = "Ilya", email = "kravtso5@uwm.edu", password = "123", role = 3, 
                              startdate = self.time, graddate = self.time)

    def test_createOrg(self):
        self.resp = self.client.post("/createOrganization/", {"email": "cssmartclub@uwm.edu", "password": "password", 
                                                     "name": "CS Smart Club", "point_of_contact": "1",
                                                     "member_count": "1", "description": "description"})
        self.assertEqual(self.resp.status_code, 200)
        self.assertEquals(self.resp.context["error_message"], "You must be logged in to create an organization")
        self.assertIsNone(org_util.get_org_by_name("CS Smart Club"))