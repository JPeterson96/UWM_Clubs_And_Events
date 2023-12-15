# name - string
# email - string
# password - string
# role - int[]
# interests - string[]
# orgs - string[]
# major - string[]
# friends - user[]

from UWM_Clubs_and_Events.models import *
import datetime
from django.db.models import Q
import re


class User_Util():
    def create_user(name, email, password, role, startdate, graddate):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

        if name == "":
            return ValueError("name is blank or cannot blank ")
        if email is None or re.match(pattern, email) is None or email == "" or ' ' in email:
            return ValueError("email does not exists or is not a proper email")
        if User_Util.get_user(email) is not None:
            return ValueError("user with email exists ")
        if password == "" or ' ' in password:
            return ValueError("password format incorrect")
        if startdate is None or startdate == "":
            return ValueError("you must enter a start date")
        if startdate is None or startdate == "":
            return ValueError("must put a start date ")

        user = None
        try:
            user = User.objects.create(email=email, password=password, name=name, role=role)
            student = Student.objects.create(user=user, enrollment_date=startdate, graduation_date=graddate)
        except Exception as e:
            user.delete()
            raise ValueError(e)

        user.save()
        student.save()

        return True

    def edit_user(name, email, new_pass, graddate):

        curr_user = User_Util.get_user(email=email)
        stu = Student.objects.get(user=curr_user)
        firstname,lastname=User_Util.user_get_last_name(name)

        if name=='' or firstname=='' or lastname=='' :
            return ValueError("must return a non empty name first and last name")
        if stu:
            if graddate != '':
                stu.graduation_date = graddate
        if new_pass == "" or ' ' in new_pass:
            return ValueError("password format incorrect")
        else:
            curr_user.password = new_pass
        curr_user.name = name
        curr_user.save()
        stu.save()

    def user_get_last_name(user_name):
        temp_name = user_name.split(" ", 1)
        if temp_name.__len__() == 1:
            last_name = ''
        else:
            last_name = temp_name[1]
        return temp_name[0], last_name

    def get_grad_dates(student):
        if student:
            formatted_enroll = student.enrollment_date.strftime("%Y-%m-%d")
            formatted_graddate = student.graduation_date.strftime("%Y-%m-%d")
        else:
            formatted_enroll = None
            formatted_graddate = None
        return (formatted_enroll, formatted_graddate)

    def set_user_interest(email, interest):
        curruser = User.objects.get(email__iexact=email)
        realInterest = None
        try:
            relInterest = Interest.objects.get(tag__exact=interest)
        except Exception as e:
            raise ValueError(e)
        person = User_Util.get_student(email=email)
        userinterest = StudentInterest.objects.create(student=person, type=relInterest)
        userinterest.save()

    def remove_major(majorstoremove, student):
        for remmaj in majorstoremove:
            actMaj = Major.objects.get(name=remmaj)
            StudentMajor.objects.filter(Q(student=student, major=actMaj)).delete()

    def add_student_major(addedmajor, curr_user_email, userMaj):
        for newmaj in addedmajor:
            if newmaj not in userMaj.values_list('major', flat=True):
                User_Util.set_student_major(curr_user_email, newmaj)

    def remove_interest_from_user(interestremove, student):
        for remint in interestremove:
            interest = Interest.objects.get(tag=remint)
            StudentInterest.objects.filter(Q(student=student, type=interest)).delete()

    def add_interest_to_user(addint, userint, curr_user_email):
        for intadd in addint:
            if intadd not in userint.values_list('type', flat=True):
                User_Util.set_user_interest(curr_user_email, intadd)

    def set_student_major(email, majorname):
        try:
            if email == "":
                return ValueError("email cannot be empty")
            student = User_Util.get_student(email=email)
            resMajor = Major.objects.get(name__iexact=majorname)
            user_major = StudentMajor.objects.create(student=student, major=resMajor)
            user_major.save()
            print("added")
            return True
        except Exception as e:
            raise ValueError(e)

    def get_user(email):
        try:
            return User.objects.get(email=email)
        except:
            return None

    def get_student(email):
        try:
            user = User_Util.get_user(email=email)
            return Student.objects.get(user=user)
        except:
            return None

    def get_all_users(self):
        try:
            return User.objects.all()
        except:
            return None

    def get_all_students(self):
        try:
            return User.objects.filter(role=1)
        except:
            return None

    def get_user_by_name(name):
        try:
            return User.objects.filter(name=name)
        except:
            return None

    def get_students_by_major(major):
        try:
            return Student.objects.filter(major=major)
        except:
            return None

    def get_students_by_interest(interest):
        try:
            return Student.objects.filter(interests=interest)
        except:
            return None
