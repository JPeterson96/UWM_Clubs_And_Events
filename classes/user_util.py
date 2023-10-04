# name - string
# email - string
# password - string
# role - int[]
# interests - string[]
# orgs - string[]
# major - string[]
# friends - user[]
import re

from UWM_Clubs_and_Events.models import User, UserInterest, Interest,UserMajor


class User_Util:
    def create_user(name, email, password, role):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

        try:
            # User.objects.create(name, email, password, role)
            if email is None or re.match(pattern, email) is None or email == "":
                raise TypeError("email does not exists or is not a proper email")
            elif  User_Util.get_user(email) is not None:
                raise TypeError("user with email exists ")
            if name == "":
                raise TypeError("name is blank ")
            user = User(email=email, password=password, name=name, role=role)
            user.save()
            return True
        except Exception as e:
            print(e)
            return False

    def set_user_interest(email, interest):
        try:
            if email =="":
                return ValueError("email cannot be empty")
            if interest == "":
                return ValueError("interest cannot be empty")
            print(type(interest))
            user = User_Util.get_user(email=email)
            relInterest = Interest.objects.get(tag__exact=interest)
            userinterest = UserInterest.objects.create(user=user, type=relInterest)
            userinterest.save()
            return True
        except Exception as e:
            print(e)
            return False

    def get_user(email):
        try:
            return User.objects.get(email__iexact=email)
        except:
            return None

    def get_all_users(self):
        try:
            return User.objects.all()
        except:
            return None

    def get_user_by_name(self, name):
        try:
            return User.objects.get(name=name)
        except:
            return None

    def get_users_by_major(self, major):
        try:
            return User.objects.filter(major=major)
        except:
            return None

    def get_users_by_interest(self, interest):
        try:
            return User.objects.filter(interests=interest)
        except:
            return None
