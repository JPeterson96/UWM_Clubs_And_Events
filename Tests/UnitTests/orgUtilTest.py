from django.test import TestCase
from classes.organization_util import Organization_Util
from UWM_Clubs_and_Events.models import Organization
from UWM_Clubs_and_Events.models import User

class TestGetOrg(TestCase):
    def setUp(self):
        self.user = User.objects.create(name="TestOrg", email="testOrg@uwm.edu", password="123", role=3)
        self.orgUser = User.objects.create(email="csssmartclub@uwm.edu", password="123", name="CS Smart Club", role=2) 
        self.org = Organization.objects.create(user=self.orgUser, name="TestOrg", point_of_contact="kravtso5@uwm.edu", 
                                               membersCount=1, description="Test Org")

    def test_getOrg(self):
        self.org2 = Organization_Util.get_org_by_name("TestOrg")
        self.assertEqual(self.org, self.org2, "Organization should match")

    def test_getOrgInvalid(self):
        self.org2 = Organization_Util.get_org_by_name("TestOrg2")
        self.assertEqual(self.org2, None, "Organization should be None")

class TestGetOrgByUser(TestCase):

    def setUp(self):
        self.user = User.objects.create(name="TestOrg", email="testOrg@uwm.edu", password="123", role=3)
        self.orgUser = User.objects.create(email="csssmartclub@uwm.edu", password="123", name="CS Smart Club", role=2) 
        self.org = Organization.objects.create(user=self.orgUser, name="TestOrg", point_of_contact="kravtso5@uwm.edu", 
                                               membersCount=1, description="Test Org")
        
    def test_getOrgByUser(self):
        self.org2 = Organization_Util.get_org_by_user_email("csssmartclub@uwm.edu")
        self.assertEqual(self.org, self.org2, "Organization should match")

    def test_getOrgByUserInvalid(self):
        self.org2 = Organization_Util.get_org_by_user_email("kravtso5@uwm.edu")
        self.assertEqual(self.org2, None, "Organization should be None")

#class to test edit orgs
class TestEditOrg(TestCase):
    def setUp(self):
        self.user = User.objects.create(name="Ilya", email="kravtso5@uwm.edu", password="123", role=3)
        self.poc = User.objects.create(name="POC", email="POC@uwm.edu", password="123", role=3)
        self.orgUser = User.objects.create(email="csssmartclub@uwm.edu", password="123", name="CS Smart Club", role=2) 
        self.org = Organization.objects.create(user=self.orgUser, name="TestOrg", point_of_contact="kravtso5@uwm.edu", 
                                               membersCount=1, description="Test Org")
        
    def test_editOrg(self):
        Organization_Util.edit_org("csssmartclub@uwm.edu", "POC@uwm.edu", 2, "new description")
        self.assertEqual(self.org.point_of_contact, "POC@uwm.edu", "Point of contact should be updated")
        self.assertEqual(self.org.membersCount, 2, "Members count should be updated")
        self.assertEqual(self.org.description, "new description", "Description should be updated")

    def test_editOrgInvalidEmail(self):
        with self.assertRaises(ValueError, msg="Email should not be empty"):
            Organization_Util.edit_org("", "POC@uwm.edu", 2, "new description")

    def test_editOrgInvalidPOC(self):
        with self.assertRaises(ValueError, msg="Point of contact should not be empty"):
            Organization_Util.edit_org("csssmartclub@uwm.edu", "", 2, "new description")

    def test_editOrgInvalidMembersCount2(self):
        with self.assertRaises(ValueError, msg="Members count should be greater than or equal to 0"):
            Organization_Util.edit_org("csssmartclub@uwm.edu", "POC@uwm.edu", -1, "new description")

    def test_editOrgInvalidDescription(self):
        with self.assertRaises(ValueError, msg="Description should not be empty"):
            Organization_Util.edit_org("csssmartclub@uwm.edu", "POC@uwm.edu", 2, "")