from django.test import TestCase
from classes.organization_util import Organization_Util
from UWM_Clubs_and_Events.models import Organization

class TestGetOrganization(TestCase):
    def test_getOrganizationValid(self):
        self.organization = Organization(name = "Test", point_of_contact = "point_of_contact", membersCount = 0, description = "description")
        self.organization.save()
        self.assertEqual(Organization_Util.get_organization("Test"), self.organization, "Organization should have been found")

class TestGetOrganizationInvalid(TestCase):
    def test_getOrganizationInvalid(self):
        self.assertEqual(Organization_Util.get_organization("Test"), None, "Organization should not have been found")

class TestGetAllOrganizations(TestCase):
    def test_getAllOrganizations(self):
        self.organization = Organization()
        self.organization.save()
        self.assertTrue(self.organization in Organization_Util.get_all_organizations(), "Organization should have been found in all organizations")
