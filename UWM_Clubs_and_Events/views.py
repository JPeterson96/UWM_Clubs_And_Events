from django.db.models import Q
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from UWM_Clubs_and_Events.models import *
from classes import user_util
from django.core.paginator import Paginator


class login(View):
    def get(self, request):
        logout(request)
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
    
class FilteredHomepage(View):
    def get(self, request, tag):
        all_events = {}

        for i in tag:
            events = Event.objects.filter(eventtag__interest__tag__exact=i)
            all_events.join(events)
        
        paginator = Paginator(all_events, 5)
        page_number = request.GET.get('page')
        events = paginator.get_page(page_number)
        current_user = user_util.User_Util.get_user(email=request.session['user'])

        return render(request, "homepage.html", {"Events": all_events, "user": current_user})
        


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

        try:
            res = user_util.User_Util.create_user(name=firstName + " " + lastName, email=email, password=password,
                                                role=0, startdate=startdate, graddate=graddate)
        except Exception as e:
            return render(request, "createaccount.html", {"error_message": e})
        
        if isinstance(res, ValueError):
            return render(request, "createaccount.html", {"message": res, "interests": search, "majors": allmajors})

            # this is returning the email not the user object?
        # check_user = user_util.User_Util.get_user(email=email)

        # adds every tage fo interest to user

        for tags in interests:
            try:
                value = user_util.User_Util.set_student_interest(email=email, interest=tags)
            except Student.DoesNotExist:
                return render(request, "createaccount.html", {"error_message": "Student does not exist"})
            # should not get here
            if isinstance(value, ValueError):
                return render(request, "createaccount.html", {"message": res, "interests": search, "majors": allmajors})

        for maj in major:
            print(maj)
            add_major = user_util.User_Util.set_student_major(email=email, majorname=maj)

            if isinstance(add_major, ValueError):
                return render(request, "createaccount.html", {"message": res, "interests": search, "majors": allmajors})
        return render(request, "login.html", {"success_message": "user account successfully created"})


class ViewAccount(View):
    def get(self, request):
        # current_user = user_util.User_Util.get_student(email=request.session['user'])
        email = request.session['user']
        userMaj = StudentMajor.objects.filter(student__user__email__exact=email) ##student__user__email ??
        userInOrgs = MembersIn.objects.filter(user__email__exact=email)
        userInt = StudentInterest.objects.filter(student__user__email__exact=email)
        current_user = user_util.User_Util.get_user(email=request.session['user'])

        return render(request, "viewaccount.html",
                      {"user": current_user, "MemsInOrg": userInOrgs, "usermajors": userMaj, "userinterest": userInt})


class EditAccount(View):
    def get(self, request):
        allints = Interest.objects.all()
        allmajors = Major.objects.all()
        current_user = user_util.User_Util.get_user(email=request.session['user'])

        current_user = user_util.User_Util.get_user(email=request.session['user'])
        userMaj = StudentMajor.objects.filter(student__user__email__exact=current_user.email) ##student__user__email
        userInOrgs = MembersIn.objects.filter(user__email__exact=current_user.email)
        userint = StudentInterest.objects.filter(student__user__email=current_user.email)

        temp_name = current_user.name.split()

        return render(request, "editaccount.html",
                      {"User": current_user, "MemsInOrg": userInOrgs, "usermajors": userMaj, "userinterest": userint,
                       "interests": allints, "firstname": temp_name[0], "lastname": temp_name[1],
                       "majors": Major.objects.all(),
                       "startdate": Student.enrollment_date, "graddate": Student.graduation_date, "user": current_user})

    def post(self, request):
        search = Interest.objects.all()
        allmajors = Major.objects.all()

        current_user = user_util.User_Util.get_user(email=request.session['user'])
        userMaj = StudentMajor.objects.filter(student__user__email__exact=current_user.email)
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
                StudentMajor.objects.filter(Q(user=current_user, major=actMaj)).delete()

        for newmaj in addedmajor:
            user_util.User_Util.set_user_major(current_user.email, newmaj)

        ##now add and remove intereests
        if interestremove:
            for remint in interestremove:
                interest = Interest.objects.get(tag=remint)
                StudentInterest.objects.filter(Q(user=current_user, type=interest)).delete()

        if addint:
            # now dd if any in the list
            for intadd in addint:
                user_util.User_Util.set_user_interest(current_user.email, intadd)

        res = user_util.User_Util.edit_user(firstName + " " + lastName, current_user.email,
                                            startdate, graddate)
        if isinstance(res, ValueError):
            return render(request, "editaccount.html", {"message": res})

        userint = StudentInterest.objects.filter(student__user__email=current_user.email)
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
        # future TODO: filter further to only get users from certain organization
        point_of_contacts = User.objects.filter(role__exact=2)
        return render(request, 'createorganization.html', {"user": current_user, "point_of_contacts": point_of_contacts})

    def post(self, request):
        orgname = request.POST.get('name')
        contact_id = request.POST.get('point_of_contact')
        print(contact_id)
        try:
            contactuser = User.objects.get(id=contact_id)
        except User.DoesNotExist:
            return render(request, "createorganization.html", {"error_message": "User does not exist"})
        membersCount = request.POST.get('member_count')
        description = request.POST.get('description')

        newOrg = Organization.objects.create(
            user=contactuser,
            name=orgname,
            point_of_contact=contactuser.email,
            membersCount=membersCount,
            description=description
        )

        newOrg.save()

        # return render(request, "homepage.html", {"success_message": "Organization Successfully created"})
        return redirect("homepage")


class CreateEvent(View):
    def get(self, request):
        tags = Interest.objects.all()
        current_user = user_util.User_Util.get_user(email=request.session['user'])
        orgs = Organization.objects.filter(user__email__exact=current_user.email)
        return render(request, "createevent.html",{"tags": tags, "orgs": orgs, "user": current_user})

    def post(self, request):
        name = request.POST.get('name')
        org_name = request.POST.get('org')
        location = request.POST.get('location')
        time_happening = request.POST.get('time-happening')
        description = request.POST.get('description')
        time_published = datetime.now()

        try:
            selected_org = Organization.objects.get(name=org_name)
        except Organization.DoesNotExist:
            return render(request, "your_template_name.html", {"error_message": "Selected organization does not exist"})


        event = Event.objects.create(name=name, organization=selected_org, location=location,
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
