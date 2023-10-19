from django.db.models import Q
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from UWM_Clubs_and_Events.models import *
from classes import user_util
from django.core.paginator import Paginator


class login(View):
    def get(self, request):
        return render(request, 'login.html', {"name": "login"})

    def post(self, request):
        noSuchUser = False
        badPassword = False
        try:
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = User.objects.get(email=request.POST.get('email'))
            badPassword = (user.password != request.POST.get('password'))
        except:
            noSuchUser = True
        if email == '' and password == '':
            return render(request, "login.html", {"error_message": "Nothing entered"})
        elif email == '':
            return render(request, "login.html", {"error_message": "No email"})
        elif password == '':
            return render(request, "login.html", {"error_message": "no password"})
        elif noSuchUser:
            return render(request, "login.html", {"error_message": "no user in database"})
        elif badPassword:
            return render(request, "login.html", {"error_message": "no user with this password"})
        else:
            request.session['user'] = user.email
            return redirect("homepage")


class Homepage(View):
    def get(self, request):
        all_events = Event.objects.all()
        paginator = Paginator(all_events, 5)  # 5 events per page

        page_number = request.GET.get('page')
        events = paginator.get_page(page_number)
        current_user = user_util.User_Util.get_user(email=request.session['user'])
        return render(request, "homepage.html", {"Events": events, "user": current_user})


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

        res = user_util.User_Util.create_user(name=firstName + " " + lastName, email=email, password=password,
                                              role=0, startdate=startdate, graddate=graddate)
        if isinstance(res, ValueError):
            return render(request, "createaccount.html", {"message": res, "interests": search, "majors": allmajors})

            # this is returning the email not the user object?
        check_user = user_util.User_Util.get_user(email=email)

        # adds every tage fo interest to user

        for tags in interests:
            value = user_util.User_Util.set_user_interest(email=check_user.email, interest=tags)
            # should not get here
            if isinstance(value, ValueError):
                return render(request, "createaccount.html", {"message": res, "interests": search, "majors": allmajors})

        for maj in major:
            print(maj)
            add_major = user_util.User_Util.set_user_major(email=check_user.email, majorname=maj)

            if isinstance(add_major, ValueError):
                return render(request, "createaccount.html", {"message": res, "interests": search, "majors": allmajors})
        return render(request, "login.html", {"success_message": "user account successfully created"})


class ViewAccount(View):
    def get(self, request):
        current_user = user_util.User_Util.get_user(email=request.session['user'])
        userMaj = UserMajor.objects.filter(user__email__exact=current_user.email)
        userInOrgs = MembersIn.objects.filter(user__email__exact=current_user.email)
        userInt = UserInterest.objects.filter(user__email=current_user.email)
        current_user = user_util.User_Util.get_user(email=request.session['user'])

        return render(request, "viewaccount.html",
                      {"User": current_user, "MemsInOrg": userInOrgs, "usermajors": userMaj, "userinterest": userInt, "user": current_user})


class EditAccount(View):
    def get(self, request):
        allints = Interest.objects.all()
        allmajors = Major.objects.all()
        current_user = user_util.User_Util.get_user(email=request.session['user'])

        current_user = user_util.User_Util.get_user(email=request.session['user'])
        userMaj = UserMajor.objects.filter(user__email__exact=current_user.email)
        userInOrgs = MembersIn.objects.filter(user__email__exact=current_user.email)
        userint = UserInterest.objects.filter(user__email=current_user.email)

        temp_name = current_user.name.split()

        return render(request, "editaccount.html",
                      {"User": current_user, "MemsInOrg": userInOrgs, "usermajors": userMaj, "userinterest": userint,
                       "interests": allints, "firstname": temp_name[0], "lastname": temp_name[1],
                       "majors": Major.objects.all(),
                       "startdate": User.gradStartDate, "graddate": User.gradEndDate, "user": current_user})

    def post(self, request):
        search = Interest.objects.all()
        allmajors = Major.objects.all()

        current_user = user_util.User_Util.get_user(email=request.session['user'])
        userMaj = UserMajor.objects.filter(user__email__exact=current_user.email)
        userInOrgs = MembersIn.objects.filter(user__email__exact=current_user.email)

        firstName = request.POST.get("firstname")
        lastName = request.POST.get("lastname")
        majorstoremove = request.POST.getlist("majorremoval")
        addedmajor = request.POST.getlist("majorlist")
        interestremove = request.POST.getlist("interestremoval")
        addint = request.POST.getlist("interesttoadd")
        startdate = request.POST.get("startdate")
        graddate = request.POST.get("graddate")
        # delete major associated with user

        if majorstoremove:
            for remmaj in majorstoremove:
                print(remmaj)
                print(remmaj, "hello ? ")
                actMaj = Major.objects.get(name=remmaj)
                print(actMaj)
                UserMajor.objects.filter(Q(user=current_user, major=actMaj)).delete()

        for newmaj in addedmajor:
            user_util.User_Util.set_user_major(current_user.email, newmaj)

        ##now add and remove intereests
        if interestremove:
            for remint in interestremove:
                interest = Interest.objects.get(tag=remint)
                UserInterest.objects.filter(Q(user=current_user, type=interest)).delete()

        if addint:
            # now dd if any in the list
            for intadd in addint:
                user_util.User_Util.set_user_interest(current_user.email, intadd)

        res = user_util.User_Util.edit_user(firstName + " " + lastName, current_user.email, current_user.role,
                                            startdate, graddate)
        if isinstance(res, ValueError):
            return render(request, "editaccount.html", {"message": res})

        userint = UserInterest.objects.filter(user__email=current_user.email)
        current_user=user_util.User_Util.get_user(email=request.session['user'])
        return render(request, "viewaccount.html",
                      {"message": "user sucessfully edited", "User": current_user, "MemsInOrg": userInOrgs,
                       "usermajors": userMaj, "userinterest": userint})


class Logout(View):
    def get(self, request):
        try:
            logout(request)
        except KeyError:
            pass
        return redirect("login")


class ViewEvent(View):
    def get(self, request, name):
        current_user = user_util.User_Util.get_user(email=request.session['user'])
        try:
            event = Event.objects.get(name=name)
            return render(request, "viewevent.html", {"Event": event, "user": current_user})
        except:
            return render(request, "homepage.html", {"error_message": "Event does not exist"})


class CreateOrganization(View):
    def get(self, request):
        current_user = user_util.User_Util.get_user(email=request.session['user'])
        return render(request, 'createorganization.html', {"user": current_user})

    def post(self, request):
        orgname = request.POST.get('name')
        contact = request.POST.get('point_of_contact')
        print(contact)
        try:
            contactuser = User.objects.get(email=contact)
        except:
            return render(request, "createorganization.html", {"error_message": "User does not exist"})
        membersCount = request.POST.get('member_count')
        description = request.POST.get('description')

        newOrg = Organization.objects.create(name=orgname, point_of_contact=contactuser, membersCount=membersCount,
                                             description=description)
        newOrg.save()

        # return render(request, "homepage.html", {"success_message": "Organization Successfully created"})
        return redirect("homepage")


class CreateEvent(View):
    def get(self, request):
        tags = Interest.objects.all()
        orgs = Organization.objects.all()
        current_user = user_util.User_Util.get_user(email=request.session['user'])
        return render(request, "createevent.html",{"tags": tags, "orgs": orgs, "user": current_user})

    def post(self, request):
        name = request.POST.get('name')
        organization = request.POST.get('organization')
        location = request.POST.get('location')
        time_happening = request.POST.get('time-happening')
        description = request.POST.get('description')
        time_published = datetime.now()

        event = Event.objects.create(name=name, organization=organization, location=location,
                                     time_happening=time_happening, description=description, time_published=time_published)
        event.save()

        #line 67
        # interests = request.POST.getlist("selected_interests")
        # for tag in interests:
        #     eventTag = EventTag.objects.create(event=event, interest=tag)
        #     eventTag.save()
        #     # should not get here
        #     if isinstance(eventTag, ValueError):
        #         return render(request, "createaccount.html", {"message": res, "interests": search, "majors": allmajors})

        return redirect("homepage")
