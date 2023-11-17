# name - string
# email - string
# password - string
# role - int[]
# interests - string[]
# orgs - string[]
# major - string[]
# friends - user[]

from UWM_Clubs_and_Events.models import *
import re


class User_Util():
    def create_user(name, email, password, role, startdate, graddate):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

        try:
            # User.objects.create(name, email, password, role)
            if name == "":
                return ValueError("name is blank or cannot blank ")
            if email is None or re.match(pattern, email) is None or email == "" or ' ' in email:
                return ValueError("email does not exists or is not a proper email")
            if User_Util.get_user(email) is not None:
                return ValueError("user with email exists ")
            if password == "" or ' ' in password:
                return ValueError("password format incorrect")
            
            try:
                user = User.objects.create(email=email, password=password, name=name, role=role)
                student = Student.objects.create(user=user, enrollment_date=startdate, graduation_date=graddate)
            except Exception as e:
                raise ValueError(e)
            
            user.save()
            student.save()

            return True
        except Exception as e:
            raise ValueError(e)

    def edit_user(name, email, new_pass, startdate, graddate):

        curr_user = User_Util.get_user(email=email)
        print(email)

        if name is not None and name is not '':
            curr_user.name = name
        if startdate is not '':
            print(" this is the start", startdate)
            curr_user.gradStartDate = startdate
        if graddate is not '':
            curr_user.gradEndDate = graddate
        if new_pass == "" or ' ' in new_pass:
            return ValueError("password format incorrect")
        else:
            curr_user.password=new_pass
        curr_user.save()

    def set_student_interest(email, interest):
        try:
            if email == "":
                return ValueError("email cannot be empty")
            try:
                student = User_Util.get_student(email=email)
            except Exception as e:
                raise ValueError(e)
            try:
                relInterest = Interest.objects.get(tag__exact=interest)
            except Exception as e:
                raise ValueError(e)
            
            userinterest = StudentInterest.objects.create(student=student, type=relInterest)
            userinterest.save()
            return True
        except Exception as e:
            raise ValueError(e)

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
