from django.test import TestCase
from classes.organization_util import Organization_Util as org_util
from classes.user_util import User_Util as user_util
import datetime

class TestCreateOrg(TestCase):

    def test_createOrg(self):
        self.time = datetime.datetime(year=2020, month=1, day=1, hour=0, minute=0, second=0, tzinfo = datetime.timezone.utc)
        user_util.create_user(name = "Ilya", email = "kravtso5@uwm.edu", password = "123", role = 3, 
                                          startdate = self.time, graddate = self.time)
        self.made = org_util.create_organization("CS Smart Club", "cssclub@uwm.edu", "123", 2, "kravtso5@uwm.edu", 1, "description")
        self.assertEqual(self.made, True)

        self.org = org_util.get_org_by_name("CS Smart Club")
        self.assertEqual(self.org.user.email, "cssclub@uwm.edu")
        self.assertEqual(self.org.user.password, "123")
        self.assertEqual(self.org.user.role, 2)
        self.assertEqual(self.org.point_of_contact, "kravtso5@uwm.edu")
        self.assertEqual(self.org.membersCount, 1)
        self.assertEqual(self.org.description, "description")


class TestInvalidInput(TestCase):

    def setUp(self):
        self.time = datetime.datetime(year=2020, month=1, day=1, hour=0, minute=0, second=0, tzinfo = datetime.timezone.utc)
        user_util.create_user(name = "Ilya", email = "kravtso5@uwm.edu", password = "123", role = 0, 
                                          startdate = self.time, graddate = self.time)
        self.user = user_util.get_user("kravtso5@uwm.edu")

    def test_emptyName(self):
        with self.assertRaises(ValueError, msg="Missing Name"):
            self.test = org_util.create_organization(name="",email="csssmartclub@uwm.edu", password="123", role=2, 
                                                     point_of_contact="kravtso5@uwm.edu", members=1, description="description")
            
    def test_emptyEmail(self):
        with self.assertRaises(ValueError, msg="Missing Email"):
            self.test = org_util.create_organization(name="CS Smart Club", email="", password="123", role=2, 
                                                     point_of_contact="kravtso5@uwm.edu", members=1, description="description")
            
    def test_emptyPassword(self):
        with self.assertRaises(ValueError, msg="Missing Password"):
            self.test = org_util.create_organization(name="CS Smart Club", email="csssmartclub@uwm.edu", password="", role=2, 
                                                     point_of_contact="kravtso5@uwm.edu", members=1, description="description")
            
    def test_invalidRole(self):
        with self.assertRaises(ValueError, msg="Invalid Role"):
            self.test = org_util.create_organization(name="CS Smart Club", email="csssmartclub@uwm.edu", password="123", role=99, 
                                                     point_of_contact="kravtso5@uwm.edu", members=1, description="description")
    
    def test_emptyPOC(self):
        with self.assertRaises(ValueError, msg="Missing Point of Contact"):
            self.test = org_util.create_organization(name="CS Smart Club", email="csssmartclub@uwm.edu", password="123", role=2, 
                                                     point_of_contact="", members=1, description="description")
            
    def test_invalidPOC(self):
        with self.assertRaises(ValueError, msg="Invalid Point of Contact"):
            self.test = org_util.create_organization(name="CS Smart Club", email="csssmartclub@uwm.edu", password="123", role=2, 
                                                    point_of_contact="kravtsov@uwm.edu", members=1, description="description")
            
    def test_invalidMembers(self):
        with self.assertRaises(ValueError, msg="Invalid Members"):
            self.test = org_util.create_organization(name="CS Smart Club", email="csssmartclub@uwm.edu", password="123", role=2, 
                                                     point_of_contact="kravtso5@uwm.edu", members=-1, description="description")
            
    def test_emptyDescription(self):
        with self.assertRaises(ValueError, msg="Missing Description"):
            self.test = org_util.create_organization(name="CS Smart Club", email="csssmartclub@uwm.edu", password="123", role=2, 
                                                     point_of_contact="kravtso5@uwm.edu", members=1, description="")

