from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from UWM_Clubs_and_Events.models import *
from classes import user_util, event_util, organization_util
from django.core.paginator import Paginator
from django.http import JsonResponse
from datetime import timedelta

class EditOrganization(View):
    def get(self, request):
        cur_user = user_util.User_Util.get_user(request.session['user'])
        if cur_user.role == 3:

            org = Organization.objects.filter(point_of_contact=cur_user)

        else:
            org = Organization.objects.filter(user=cur_user)
        pocs = User.objects.filter(role=3)
        return render(request, 'editorganization.html', {'user': cur_user, 'organizations': org, 'contacts': pocs})

    def post(self, request):
        cur_user = user_util.User_Util.get_user(request.session['user'])
        org = Organization.objects.get(user=cur_user)

        new_point_of_contact = request.POST.get('point_of_contact')
        membersCount = request.POST.get('membersCount')
        new_description = request.POST.get('description')

        checkEditorg = organization_util.Organization_Util.edit_org(cur_user.email, new_point_of_contact,
                                                                    membersCount, new_description)

        if isinstance(checkEditorg, ValueError):
            return render(request, 'editorganization.html', {'user': cur_user, 'organization': org,
                                                             'message': checkEditorg})

        cur_user.save()

        return render(request, 'editorganization.html', {'user': cur_user, 'organization': org,
                                                         'message': 'Organization information changed successfully!'})