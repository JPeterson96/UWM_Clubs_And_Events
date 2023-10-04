# name
# point_of_contact
# members
# description
# role
# interests

from UWM_Clubs_and_Events.models import Organization

class Organization_Util():
    def create_organization(self, name, point_of_contact, members, description, role, interests):
        try:
            org = Organization(name=name, point_of_contact=point_of_contact, members=members, description=description, role=role, interests=interests)
            org.save()
            return True
        except Exception as e:
            print(e)
            return False

    def get_org(name):
        try:
            return Organization.objects.get(name=name)
        except:
            return None
        
    def get_all_orgs():
        try:
            return Organization.objects.all()
        except:
            return None
        
    def get_org_by_interest(interests):
        try:
            return Organization.objects.filter(interests=interests)
        except:
            return None
        
    def get_org_by_major(major):
        try:
            return Organization.objects.filter(major=major)
        except:
            return None
        
    def get_members(name):
        try:
            return Organization.objects.get(name=name).members
        except:
            return None
        