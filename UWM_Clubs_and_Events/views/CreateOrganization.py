from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from UWM_Clubs_and_Events.models import *
from classes import user_util, event_util, organization_util
from django.core.paginator import Paginator
from django.http import JsonResponse
from datetime import timedelta


class CreateOrganization(View):
    def get(self, request):
        current_user = user_util.User_Util.get_user(email=request.session['user'])
        # future TODO: filter further to only get users from certain organization
        point_of_contacts = User.objects.filter(role__exact=3)
        return render(request, 'createorganization.html',
                      {"user": current_user, "point_of_contacts": point_of_contacts})

    def post(self, request):
        current_user = user_util.User_Util.get_user(email=request.session['user'])
        point_of_contacts = User.objects.filter(role__exact=3)
        email = request.POST.get('email')
        if email == '':
            return render(request, 'createorganization.html', {'user': current_user, "point_of_contacts":
                point_of_contacts, "message": "Please enter an email"})
        password = request.POST.get('password')
        if password == '':
            return render(request, 'createorganization.html', {'user': current_user, "point_of_contacts":
                point_of_contacts, "message": "Please enter a password"})
        role = 2
        orgname = request.POST.get('name')
        if orgname == '':
            return render(request, 'createorganization.html', {'user': current_user, "point_of_contacts":
                point_of_contacts, "message": "Please enter an Organization Name"})
        contact_id = request.POST.get('point_of_contact')
        if contact_id == '':
            return render(request, 'createorganization.html', {'user': current_user, "point_of_contacts":
                point_of_contacts, "message": "Please select your Organization's Point of Contact"})

        try:
            contactuser = User.objects.get(id=contact_id)
        except User.DoesNotExist:
            return render(request, "createorganization.html", {"message": "User does not exist"})
        membersCount = request.POST.get('member_count')
        if request.POST.get('member_count') == '':
            return render(request, 'createorganization.html', {'user': current_user, "point_of_contacts":
                point_of_contacts, "message": "Please enter the number of members in the Organization"})
        membersCount = int(membersCount)
        description = request.POST.get('description')
        if description == '':
            return render(request, 'createorganization.html', {'user': current_user, "point_of_contacts":
                point_of_contacts, "message": "Please enter a description"})

        try:
            organization = organization_util.Organization_Util.create_organization(orgname, email, password, role,
                                                                                   contactuser.email, membersCount,
                                                                                   description)
        except Exception as e:
            current_user = user_util.User_Util.get_user(email=request.session['user'])
            point_of_contacts = User.objects.filter(role__exact=3)
            return render(request, "createorganization.html",
                          {"message": e, "user": current_user, "point_of_contacts": point_of_contacts})

        if isinstance(organization, ValueError):
            current_user = user_util.User_Util.get_user(email=request.session['user'])
            point_of_contacts = User.objects.filter(role__exact=3)
            return render(request, "createorganization.html",
                          {"message": organization, "user": current_user, "point_of_contacts": point_of_contacts})

        # newOrg = Organization.objects.create(
        #     user=contactuser,
        #     name=orgname,
        #     point_of_contact=contactuser.email,
        #     membersCount=membersCount,
        #     description=description
        # )
        #
        # newOrg.save()
        # create a new search tag for the organization if it doesnt exist
        current_user = user_util.User_Util.get_user(email=request.session['user'])
        # future TODO: filter further to only get users from certain organization
        point_of_contacts = User.objects.filter(role__exact=3)
        return render(request, "createorganization.html",
                      {"message": "Organization Successfully created", "user": current_user,
                       "point_of_contacts": point_of_contacts})
