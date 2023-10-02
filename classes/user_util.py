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
    def create_user(self, name, email, password, role):
        try:
            user = User(name=name, email=email, password=password, role=role)
            user.save()
            return user
        except:
            return None

    def get_user(self, email):
        try:
            return User.objects.get(email=email)
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
