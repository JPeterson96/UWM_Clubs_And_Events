from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from UWM_Clubs_and_Events.models import *
from classes import user_util, event_util, organization_util
from django.core.paginator import Paginator
from django.http import JsonResponse
from datetime import timedelta

class ViewAccount(View):
    def get(self, request):
        email = request.session['user']

        student = user_util.User_Util.get_student(email=email)
        userMaj = StudentMajor.objects.filter(student__user__email__exact=email)  ##student__user__email ??
        userInOrgs = MembersIn.objects.filter(user__email__exact=email)
        userInt = StudentInterest.objects.filter(student__user__email__exact=email)
        current_user = user_util.User_Util.get_user(email=request.session['user'])

        return render(request, "viewaccount.html",
                      {"User": current_user, "Stu": student, "MemsInOrg": userInOrgs, "usermajors": userMaj,
                       "userinterest": userInt})