from django.test import TestCase
from classes.user_util import User_Util as user_util
from UWM_Clubs_and_Events.models import User
from UWM_Clubs_and_Events.models import Student
from UWM_Clubs_and_Events.models import Interest
from UWM_Clubs_and_Events.models import StudentInterest
from UWM_Clubs_and_Events.models import Major
from UWM_Clubs_and_Events.models import StudentMajor
import datetime

class TestGetUser(TestCase):
    
    def setUp(self):
        self.user = User.objects.create(name="Ilya", email="kravtso5@uwm.edu", password="123", role=0)

    def test_getUser(self):
        self.user2 = user_util.get_user("kravtso5@uwm.edu")
        self.assertEqual(self.user, self.user2, "User should match")

    def test_getUserInvalid(self):
        self.user2 = user_util.get_user("kravtsov@uwm.edu")
        self.assertEqual(self.user2, None, "User should be None")

class TestGetStudent(TestCase):
        
        def setUp(self):
            self.time = datetime.datetime(year=2020, month=1, day=1, hour=0, minute=0, second=0, tzinfo = datetime.timezone.utc)
            self.user = User.objects.create(name="Ilya", email="kravtso5@uwm.edu", password="123", role=0)
            self.student = Student.objects.create(user=self.user, enrollment_date=datetime.datetime.now(), graduation_date=datetime.datetime.now())

        def test_getStudent(self):
            self.student2 = user_util.get_student("kravtso5@uwm.edu")
            self.assertEqual(self.student, self.student2, "Student should match")

        def test_getStudentInvalid(self):
            self.student2 = user_util.get_student("kravtsov@uwm.edu")
            self.assertEqual(self.student2, None, "Student should be None")

class testEditUser(TestCase):
    def setUp(self):
        self.user = User.objects.create(name="Ilya", email="kravtso5@uwm.edu", password="123", role=0)
        self.student = Student.objects.create(user=self.user, enrollment_date=datetime.datetime.now(), graduation_date=datetime.datetime.now())

    def test_editUser(self):
        self.time = datetime.datetime(year=2020, month=1, day=1, hour=0, minute=0, second=0, tzinfo = datetime.timezone.utc)
        user_util.edit_user("Ilya Kravtsov", "kravtso5@uwm.edu", "1234", self.time, self.time)
        self.user2 = user_util.get_user("kravtso5@uwm.edu")
        self.assertEqual(self.user2.name, "Ilya Kravtsov", "Name should be Ilya Kravtsov")
        self.assertEqual(self.user2.password, "1234", "Password should be 1234")

    def test_editUserInvalidEmail(self):
        self.time = datetime.datetime.now()
        with self.assertRaises(ValueError, msg="Email should not be empty"):
                user_util.edit_user(name="Ilya Kravtsov", email="", new_pass="1234", startdate=self.time, graddate=self.time)

    def test_editUserInvalidName(self):
        self.time = datetime.datetime.now()
        with self.assertRaises(ValueError, msg="Name should not be empty"):
            user_util.edit_user(name="", email="kravtso5@uwm.edu", new_pass="1234", startdate=self.time, graddate=self.time)

    def test_editUserInvalidPassword(self):
        self.time = datetime.datetime.now()
        with self.assertRaises(ValueError, msg="Password should not be empty"):
            user_util.edit_user(name="Ilya Kravtsov", email="kravtso5@uwm.edu", new_pass="", startdate=self.time, graddate=self.time)

    def test_editUserInvalidPassword2(self):
        self.time = datetime.datetime.now()
        with self.assertRaises(ValueError, msg="Password should not have spaces"):
            user_util.edit_user(name="Ilya Kravtsov", email="kravtso5@uwm.edu", new_pass=" ", startdate=self.time, graddate=self.time)

class testSetStudentInterest(TestCase):
    def setUp(self):
        self.user = User.objects.create(name="Ilya", email="kravtso5@uwm.edu", password="123", role=0)
        self.student = Student.objects.create(user=self.user, enrollment_date=datetime.datetime.now(), graduation_date=datetime.datetime.now())
        self.interest = Interest.objects.create(tag="Computer Science")
        # self.interest = StudentInterest.objects.create(student=self.student, type=Interest.objects.create(tag="Computer Science"))

    def test_setStudentInterest(self):
        user_util.set_student_interest("kravtso5@uwm.edu", "Computer Science")
        self.userinterest = StudentInterest.objects.get(student=self.student)
        self.assertEqual(self.userinterest.type, self.interest, "Interest should match")

    def test_setStudentInterestInvalidEmail(self):
        with self.assertRaises(ValueError, msg="Email should not be empty"):
            user_util.set_student_interest("", "Computer Science")

    def test_setStudentInterestInvalid(self):
        with self.assertRaises(ValueError, msg="Interest should not be empty"):
            user_util.set_student_interest("kravtso5@uwm.edu", "")

    def test_setStudentInterestInvalid2(self):
        with self.assertRaises(ValueError, msg="Interest should exist"):
            user_util.set_student_interest("kravtso5@uwm.edu", "Art")

class testSetStudentMajor(TestCase):
    def setUp(self):
        self.user = User.objects.create(name="Ilya", email="kravtso5@uwm.edu", password="123", role=0)
        self.student = Student.objects.create(user=self.user, enrollment_date=datetime.datetime.now(), graduation_date=datetime.datetime.now())
        self.major = Major.objects.create(name="Computer Science")

    def test_setStudentMajor(self):
        user_util.set_student_major("kravtso5@uwm.edu", "Computer Science")
        self.studentmajor = StudentMajor.objects.get(student=self.student)
        self.assertEqual(self.studentmajor.major, self.major, "Major should match")

    def test_setStudentMajorInvalidEmail(self):
        with self.assertRaises(ValueError, msg="Email should not be empty"):
            user_util.set_student_major("", "Computer Science")

    def test_setStudentMajorInvalid(self):
        with self.assertRaises(ValueError, msg="Major should not be empty"):
            user_util.set_student_major("kravtso5@uwm.edu", "")

    def test_setStudentMajorInvalid2(self):
        with self.assertRaises(ValueError, msg="Major should exist"):
            user_util.set_student_major("kravtso5@uwm.edu", "Art")