# name - string
# email - string
# password - string
# role - int[]
# interests - string[]
# orgs - string[]
# major - string[]
# friends - user[]

from UWM_Clubs_and_Events.models import User, UserInterest, Interest, UserMajor, Major
import re

class User_Util():
    def create_user(name, email, password, role):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

        try:
            # User.objects.create(name, email, password, role)
            if email is None or re.match(pattern, email) is None or email == "":
                return ValueError("email does not exists or is not a proper email")
            elif User_Util.get_user(email) is not None:
                return ValueError("user with email exists ")
            if name == "":
                return ValueError("name is blank ")
            if password == "":
                return ValueError("cannot have a blank password")
            user = User(email=email, password=password, name=name, role=role)
            user.save()
            print("returning true?")
            return True
        except Exception as e:
            raise ValueError(e)

    def set_user_interest(email, interest):
        try:
            if email =="":
                return ValueError("email cannot be empty")
            if interest == "":
                return ValueError("interest cannot be empty")
            user = User_Util.get_user(email=email)
            relInterest = Interest.objects.get(tag__exact=interest)
            userinterest = UserInterest.objects.create(user=user, type=relInterest)
            userinterest.save()
            return True
        except Exception as e:
            raise ValueError(e)

    def set_user_major(email, majorname):
        try:
            if email =="":
                return ValueError("email cannot be empty")
            if majorname == "":
                return ValueError("interest cannot be empty")
            print(majorname)
            user = User_Util.get_user(email=email)
            resMajor = Major.objects.get(name__iexact=majorname)
            user_major= UserMajor.objects.create(user=user, major=resMajor)
            user_major.save()
            return True
        except Exception as e:
            raise ValueError(e)

    def get_user(email):
        try:
            return User.objects.get(email=email)
        except:
            return None
        
    def get_all_users(self):
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
