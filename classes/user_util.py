# name - string
# email - string
# password - string
# role - int[]
# interests - string[]
# orgs - string[]
# major - string[]
# friends - user[]

from UWM_Clubs_and_Events.models import User, UserInterest, Interest
import re

class User_Util():
    def create_user(name, email, password, role):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

        try:
            # User.objects.create(name, email, password, role)
            if email is None or re.match(pattern, email) is None or email == "":
                raise ValueError("email does not exists or is not a proper email")
            elif  User_Util.get_user(email) is not None:
                raise ValueError("user with email exists ")
            if name == "":
                raise ValueError("name is blank ")
            if password == "":
                raise ValueError("cannot have a blank password")
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
            return User.objects.get(email=email)
        except:
            return None
        
    def get_all_users():
        try:
            return User.objects.all()
        except:
            return None
    
    def get_user_by_name(name):
        try:
            return User.objects.filter(name=name)
        except:
            return None
        
    def get_users_by_major(major):
        try:
            return User.objects.filter(major=major)
        except:
            return None
        
    def get_users_by_interest(interest):
        try:
            return User.objects.filter(interests=interest)
        except:
            return None
