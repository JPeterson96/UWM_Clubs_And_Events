from django.test import TestCase
from django.test import Client
from classes.user_util import User_Util as user_util
from classes.organization_util import Organization_Util as org_util
import datetime

class TestValidEditOrg(TestCase):
    def setUp(self):
        self.client = Client()
        self.time = datetime.datetime(year=2020, month=1, day=1, hour=0, minute=0, second=0, tzinfo = datetime.timezone.utc)
        user_util.create_user(name = "Ilya", email = "kravtso5@uwm.edu", password = "123", role = 3, 
                              startdate = self.time, graddate = self.time)
        self.user = user_util.get_user("kravtso5@uwm.edu")
        self.client.post("/", {"email": "kravtso5@uwm.edu", "password": "123"})
        self.resp = self.client.post("/createOrganization/", {"email": "cssmartclub@uwm.edu", "password": "password", 
                                                     "name": "CS Smart Club", "point_of_contact": "1",
                                                     "member_count": "1", "description": "description"})
        self.client.get("/login/")
        self.client.post("/", {"email": "cssmartclub@uwm.edu", "password": "password"})
        self.org= org_util.get_org_by_name("CS Smart Club")
        
    def test_editOrg(self):
        self.resp = self.client.post("/editOrganization/", {"point_of_contact": "kravtso5@uwm.edu","membersCount": 2, "description": "new description"})
        self.assertEqual(self.resp.status_code, 200)
        self.assertEquals(self.resp.context["message"], "Organization information changed successfully!")
        self.assertEquals(self.org.membersCount, 2)
        self.assertEquals(self.org.description, "new description")

class TestInvalidEditOrg(TestCase):
    def setUp(self):
        self.client = Client()
        self.time = datetime.datetime(year=2020, month=1, day=1, hour=0, minute=0, second=0, tzinfo = datetime.timezone.utc)
        user_util.create_user(name = "Ilya", email = "kravtso5@uwm.edu", password = "123", role = 3, 
                              startdate = self.time, graddate = self.time)
        self.user = user_util.get_user("kravtso5@uwm.edu")
        self.client.post("/", {"email": "kravtso5@uwm.edu", "password": "123"})
        self.resp = self.client.post("/createOrganization/", {"email": "cssmartclub@uwm.edu", "password": "password", 
                                                     "name": "CS Smart Club", "point_of_contact": "1",
                                                     "member_count": "1", "description": "description"})
        self.client.get("/login/")
        self.client.post("/", {"email": "cssmartclub@uwm.edu", "password": "password"})
        self.org= org_util.get_org_by_name("CS Smart Club")
        
    def test_editOrgInvalidMemberCount(self):
        self.resp = self.client.post("/editOrganization/", {"point_of_contact": "kravtso5@uwm.edu","membersCount": -1, "description": "new description"})
        self.assertEqual(self.resp.status_code, 200)
        self.assertEquals(self.resp.context["message"], "Invalid member count!")
        self.assertEquals(self.org.membersCount, 1)
        self.assertEquals(self.org.description, "description")

    def test_editOrgInvalidDescription(self):
        self.resp = self.client.post("/editOrganization/", {"point_of_contact": "kravtso5@uwm.edu","membersCount": 2, "description": ""})
        self.assertEqual(self.resp.status_code, 200)
        self.assertEquals(self.resp.context["message"], "Invalid description!")
        self.assertEquals(self.org.membersCount, 1)
        self.assertEquals(self.org.description, "description")

    def test_editOrgInvalidPointOfContact(self):
        self.resp = self.client.post("/editOrganization/", {"point_of_contact": "kravtsov@uwm.edu","membersCount": 2, "description": "new description"})
        self.assertEqual(self.resp.status_code, 200)
        self.assertEquals(self.resp.context["message"], "Invalid point of contact!")
        self.assertEquals(self.org.membersCount, 1)
        self.assertEquals(self.org.description, "description")

class TestEditOrgNotLoggedIn(TestCase):
    def setUp(self):
        self.client = Client()
        self.time = datetime.datetime(year=2020, month=1, day=1, hour=0, minute=0, second=0, tzinfo = datetime.timezone.utc)
        user_util.create_user(name = "Ilya", email = "kravtso5@uwm.edu", password = "123", role = 3, 
                              startdate = self.time, graddate = self.time)
        self.user = user_util.get_user("kravtso5@uwm.edu")
        self.client.post("/", {"email": "kravtso5@uwm.edu", "password": "123"})
        self.resp = self.client.post("/createOrganization/", {"email": "cssmartclub@uwm.edu", "password": "password", 
                                                     "name": "CS Smart Club", "point_of_contact": "1",
                                                     "member_count": "1", "description": "description"})
        self.client.get("/login/")
        self.client.post("/", {"email": "cssmartclub@uwm.edu", "password": "password"})
        self.org= org_util.get_org_by_name("CS Smart Club")

