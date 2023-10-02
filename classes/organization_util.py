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
            return org
        except:
            return None

    def get_org(self, name):
        try:
            return Organization.objects.get(name=name)
        except:
            return None
        
    def get_all_orgs(self):
        try:
            return Organization.objects.all()
        except:
            return None
        
    def get_org_by_interest(self, interests):
        try:
            return Organization.objects.filter(interests=interests)
        except:
            return None
        
    def get_org_by_major(self, major):
        try:
            return Organization.objects.filter(major=major)
        except:
            return None
        
    def get_members(self, name):
        try:
            return Organization.objects.get(name=name).members
        except:
            return None
        