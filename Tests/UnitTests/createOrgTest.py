from django.test import TestCase
from classes import organization

class TestCreateOrg(TestCase):

    def test_createOrg(self):
        self.made = createOrg(self, name = "CS Smart Club", point_of_contact = "poc", description = "description")
        self.assertEqual(self.made, True)

        self.org = getOrg(self, "CS Smart Club")
        self.assertEqual(self.org.point_of_contact, "poc")
        self.assertEqual(self.org.description, "description")

class TestInvalidInput(TestCase):

    def test_emptyName(self):
        self.made = createOrg(self, name = "", point_of_contact = "poc", description = "description")
        self.assertEqual(self.made, False)
    
    def test_emptyDescription(self):
        self.made = createOrg(self, name = "CS Smart Club", point_of_contact = "poc", description = "")
        self.assertEqual(self.made, False)
