from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from UWM_Clubs_and_Events.models import *
from classes import user_util, event_util, organization_util
from django.core.paginator import Paginator
from django.http import JsonResponse
from datetime import timedelta

class EditAccount(View):
    def get(self, request):
        allints = Interest.objects.all()
        allmajors = Major.objects.all()
        current_user = user_util.User_Util.get_user(email=request.session['user'])
        userInOrgs = MembersIn.objects.filter(user__email__exact=current_user.email)


        student = user_util.User_Util.get_student(current_user.email)
        userMaj = StudentMajor.objects.filter(student__user__email__exact=current_user.email)  ##student__user__email
        userint = StudentInterest.objects.filter(student__user__email=current_user.email)

        first_name, last_name = user_util.User_Util.user_get_last_name(current_user.name)

        if student:
            formatted_enroll, formatted_graddate = user_util.User_Util.get_grad_dates(student)


        return render(request, "editaccount.html",
                      {"User": current_user, "Stu": student, "MemsInOrg": userInOrgs, "usermajors": userMaj,
                       "userinterest": userint,
                       "interests": allints, "firstname": first_name, "lastname": last_name,
                       "majors": Major.objects.all(), "enrollment_date": formatted_enroll,
                       "graduation_date": formatted_graddate})

    def post(self, request):
        search = Interest.objects.all()
        allmajors = Major.objects.all()
        allints = Interest.objects.all()

        current_user = user_util.User_Util.get_user(email=request.session['user'])
        userMaj = StudentMajor.objects.filter(student__user__email__exact=current_user.email)
        userInOrgs = MembersIn.objects.filter(user__email__exact=current_user.email)
        student = user_util.User_Util.get_student(current_user.email)
        userMaj = StudentMajor.objects.filter(student__user__email__exact=current_user.email)  ##student__user__email
        userint = StudentInterest.objects.filter(student__user__email=current_user.email)


        firstName = request.POST.get("firstname")
        lastName = request.POST.get("lastname")
        majorstoremove = request.POST.getlist("majorremoval")
        addedmajor = request.POST.getlist("majorlist")
        interestremove = request.POST.getlist("interestremoval")
        addint = request.POST.getlist("interesttoadd")
        startdate = request.POST.get("startdate")
        graddate = request.POST.get("graddate")
        new_pass = request.POST.get("password")
        # delete major associated with user

        if majorstoremove:
            user_util.User_Util.remove_major(majorstoremove, student)

        if addedmajor:
            user_util.User_Util.add_student_major(addedmajor, current_user.email, userMaj)

        ##now add and remove intereests
        if interestremove:
            user_util.User_Util.remove_interest_from_user(interestremove, student)

        if addint:
            # now dd if any in the list
            user_util.User_Util.add_interest_to_user(addint, userint, current_user.email)

        res = user_util.User_Util.edit_user(firstName + " " + lastName, current_user.email, new_pass,
                                            graddate)
        if isinstance(res, ValueError):
            return render(request, "editaccount.html",
                          {"message": res, "User": current_user, "Stu": student, "MemsInOrg": userInOrgs,
                           "usermajors": userMaj,
                           "userinterest": userint,
                           "interests": allints, "firstname": firstName, "lastname": lastName,
                           "majors": Major.objects.all(), "enrollment_date": startdate,
                           "graduation_date": graddate})

        userint = StudentInterest.objects.filter(student__user__email=current_user.email)
        current_user = user_util.User_Util.get_user(email=request.session['user'])
        student = user_util.User_Util.get_student(email=current_user.email)
        return render(request, "viewaccount.html",
                      {"message": "user sucessfully edited", "User": current_user, "Stu": student,
                       "MemsInOrg": userInOrgs,
                       "usermajors": userMaj, "userinterest": userint})