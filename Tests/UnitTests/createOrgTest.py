from django.test import TestCase

class test_createOrg(TestCase):

    def test_createOrg(self):
        self.made = createOrg(self, name = "CS Smart Club", point_of_contact = "poc", description = "description")
        self.assertEqual(self.made, True)

        self.org = getOrg(self, "CS Smart Club")
        self.assertEqual(self.org.point_of_contact, "poc")
        self.assertEqual(self.org.description, "description")

class test_invalid_input(TestCase):

    def test_emptyName(self):
        self.made = createOrg(self, name = "", point_of_contact = "poc", description = "description")
        self.assertEqual(self.made, False)
    
    def test_emptyDescription(self):
        self.made = createOrg(self, name = "CS Smart Club", point_of_contact = "poc", description = "")
        self.assertEqual(self.made, False)
