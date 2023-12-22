from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from UWM_Clubs_and_Events.models import *
from classes import user_util, event_util, organization_util
from django.core.paginator import Paginator
from django.http import JsonResponse
from datetime import timedelta


class CreateAccount(View):
    def get(self, request):
        search = request.GET.get('search-input', '')
        filtered_interests = Interest.objects.filter(tag__icontains=search)
        majors = Major.objects.all()
        return render(request, "createaccount.html", {"interests": filtered_interests, "majors": majors})

    def post(self, request):
        search = Interest.objects.all()
        allmajors = Major.objects.all()

        firstName = request.POST.get("firstname")
        lastName = request.POST.get("lastname")
        email = request.POST.get("email")
        password = request.POST.get("password")
        major = request.POST.getlist("majorlist")
        interests = request.POST.getlist("selected_interests")
        startdate = request.POST.get("startdate")
        graddate = request.POST.get("graddate")

        print(startdate)

        try:
            res = user_util.User_Util.create_user(name=firstName + " " + lastName, email=email, password=password,
                                                  role=0, startdate=startdate, graddate=graddate)
        except Exception as e:
            return render(request, "createaccount.html",
                          {"message": e, "interests": search, "fName": firstName, "lName": lastName, "email": email,
                           "startdate": startdate, "majors": allmajors})

        if isinstance(res, ValueError):
            return render(request, "createaccount.html",
                          {"message": res, "interests": search, "fName": firstName, "lName": lastName, "email": email,
                           "startdate": startdate, "majors": allmajors})

        # adds every tage fo interest to user

        for tags in interests:
            try:
                value = user_util.User_Util.set_user_interest(email=email, interest=tags)
            except Student.DoesNotExist:
                return render(request, "createaccount.html",
                              {"message": "student does not exists", "interests": search, "fName": firstName,
                               "lName": lastName, "email": email, "startdate": startdate, "majors": allmajors})
            # should not get here
            if isinstance(value, ValueError):
                return render(request, "createaccount.html",
                              {"message": value, "interests": search, "fName": firstName, "lName": lastName,
                               "email": email, "startdate": startdate, "majors": allmajors})

        for maj in major:
            add_major = user_util.User_Util.set_student_major(email=email, majorname=maj)

            if isinstance(add_major, ValueError):
                return render(request, "createaccount.html",
                              {"message": add_major, "interests": search, "fName": firstName, "lName": lastName,
                               "email": email, "startdate": startdate, "majors": allmajors})
        return render(request, "login.html", {"message": "user account successfully created"})
