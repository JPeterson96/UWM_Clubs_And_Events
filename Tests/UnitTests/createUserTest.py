from django.test import TestCase

class test_createUser(TestCase):

    def test_createUser(self):
        self.made = createUser(self, name = "Ilya", email = "kravtso5@uwm.edu", password = "123")
        self.assertEqual(self.made, True)

        self.user = getUser(self, "kravtso5@uwm.edu")
        self.assertEqual(self.user.name , "Ilya")
        self.assertEqual(self.user.password , "123")

class test_invalid_input(TestCase):

    def test_emptyName(self):
        self.made = test_createUser(self, name = "", email = "kravtso5@uwm.edu", password = "123")
        self.assertEqual(self.made, False)

    def test_emptyEmail(self):
        self.made = test_createUser(self, name = "Ilya", email = "", password = "123")
        self.assertEqual(self.made, False)

    def test_emptyPassword(self):
        self.made = test_createUser(self, name = "Ilya", email = "kravtso5@uwm.edu", password = "")
        self.assertEqual(self.made, False)

    def test_invalidEmail(self):
        self.made = test_createUser(self, name = "Bob", email = "invalid email", password = "123")
        self.assertEqual(self.made, False)