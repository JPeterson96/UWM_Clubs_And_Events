from django.test import TestCase
from classes.organization_util import Organization_Util as org_util

class TestCreateOrg(TestCase):

    def test_createOrg(self):
        self.made = org_util.create_organization(name = "CS Smart Club", point_of_contact = "poc", description = "description")
        self.assertEqual(self.made, True)

        self.org = org_util.get_org("CS Smart Club")
        self.assertEqual(self.org.point_of_contact, "poc")
        self.assertEqual(self.org.description, "description")

class TestInvalidInput(TestCase):

    def test_emptyName(self):
        self.made = org_util.create_organization(name = "", point_of_contact = "poc", description = "description")
        self.assertEqual(self.made, False)
    
    def test_emptyDescription(self):
        self.made = org_util.create_organization(name = "CS Smart Club", point_of_contact = "poc", description = "")
        self.assertEqual(self.made, False)
