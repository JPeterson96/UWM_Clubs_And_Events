# name
# point_of_contact
# members
# description
# role
# interests

from UWM_Clubs_and_Events.models import *
from classes import user_util
import re


class Organization_Util():
    def create_organization(name, email, password, role, point_of_contact, members, description):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

        try:
            if email is None or re.match(pattern, email) is None or email == "" or ' ' in email:
                return ValueError("email does not exists or is not a proper email")
            if password == '':
                return ValueError("Password cannot be empty")
            if role != 2:
                return ValueError("User role must be of Organization")
            if name == '':
                return ValueError("Name cannot be blank")
            # if type(name) is not type(str):
            #     return ValueError("Name must be of type String: " + name)
            if user_util.User_Util.get_user_by_name(point_of_contact) is None:
                return ValueError("Point of Contact is not a valid user")
            if members < 0:  # uses a number field in HTML, should never be a non integer
                return ValueError("Number of members in an organization cannot be less than 0")
            if description == '':
                return ValueError("Description should not be empty")

            try:
                user = User.objects.create(email=email, password=password, name=name, role=role)
                organization = Organization.objects.create(user=user, name=name, point_of_contact=point_of_contact,
                                                           membersCount=members, description=description)
            except Exception as e:
                raise ValueError(e)

            user.save()
            organization.save()
            return True
        except Exception as e:
            raise ValueError(e)

    def get_org_by_name(name):
        try:
            return Organization.objects.get(name=name)
        except:
            return None

    def get_org_by_user_email(email):
        try:
            return Organization.objects.get(user__email=email)
        except:
            return None

    def get_all_orgs(self):
        try:
            return Organization.objects.all()
        except:
            return None

    # need to discuss implementation of this w/ group
    # def get_org_by_interest(interests):
    #     try:
    #         return Organization.objects.filter(interests=interests)
    #     except:
    #         return None

    # def get_org_by_major(major):
    #     try:
    #         return Organization.objects.filter(major=major)
    #     except:
    #         return None

    # this will grab all the users registered with the organization from the MembersIn model
    def get_members(name):
        try:
            return MembersIn.objects.filter(organization__name=name)
        except:
            return None

    def edit_org(email, password, point_of_contact, membersCount, description):
        print(email)
        if user_util.User_Util.get_user(point_of_contact) is None:
            return ValueError("Point of Contact is not a valid user")
        if int(membersCount) < 0:
            return ValueError("Number of members cannot be negative")
        if description is not None and description == '':
            return ValueError("Description cannot be empty")
        # if description is not isinstance(description, str):
        #     return ValueError("Description must be of type String")
        if password == "" or ' ' in password:
            return ValueError("password format incorrect")

        # this get user account of org
        try:
            org_acc = User.objects.get(email__iexact=email)
            print("this sit the org object", org_acc.email, org_acc.password)
        except User.DoesNotExist:
            return ValueError("user does not exists with this email")

        org_acc.password=password

        organization = Organization_Util.get_org_by_user_email(org_acc.email)

        organization.point_of_contact = point_of_contact
        organization.membersCount = membersCount
        organization.description = description
        org_acc.save()
        organization.save()
