# name - string
# email - string
# password - string
# role - int[]
# interests - string[]
# orgs - string[]
# major - string[]
# friends - user[]

from UWM_Clubs_and_Events.models import User

class User_Util():
    def create_user(name, email, password, role):
        try:
            # User.objects.create(name, email, password, role)
            user = User(email=email, password=password, name=name, role=role)
            user.save()
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
