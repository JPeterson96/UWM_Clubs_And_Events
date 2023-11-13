from django.db.models import Q
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from UWM_Clubs_and_Events.models import *
from classes import user_util, event_util
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

    def post(self, request):
        sort = request.POST.get('sortType')
        order = request.POST.get('sortOrder')
        date = request.POST.get('dateRange')
        # clear = request.POST.get('clear')
        # interests = request.POST.getlist('interests')
        current_user = user_util.User_Util.get_user(email=request.session['user'])

        # convert to int
        sort = int(sort)
        order = int(order)
        date = int(date)

        filtered_events = event_util.Event_Util.filter_events(
            user=current_user,
            sort_type=sort,
            order=order,
            by_date=date,
            clear=False,
            interests=None)

        paginator = Paginator(filtered_events, 5)
        page_number = request.GET.get('page')
        events = paginator.get_page(page_number)

        return render(request, "homepage.html", {"Events": events, "user": current_user})


class FilteredHomepage(View):
    def get(self, request):
        all_events = []

        current_user = user_util.User_Util.get_user(email=request.session['user'])
        all_events = event_util.Event_Util.filter_events(
            user=current_user,
            sort_type=1,
            order=1,
            by_date=1,
            clear=False,
            interests=None)

        paginator = Paginator(all_events, 5)
        page_number = request.GET.get('page')
        events = paginator.get_page(page_number)

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
            add_major = user_util.User_Util.set_student_major(email=email, majorname=maj)

            if isinstance(add_major, ValueError):
                return render(request, "createaccount.html", {"message": res, "interests": search, "majors": allmajors})
        return render(request, "login.html", {"success_message": "user account successfully created"})


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


class EditAccount(View):
    def get(self, request):
        allints = Interest.objects.all()
        allmajors = Major.objects.all()
        current_user = user_util.User_Util.get_user(email=request.session['user'])
        userInOrgs = MembersIn.objects.filter(user__email__exact=current_user.email)

        student = user_util.User_Util.get_student(current_user.email)
        userMaj = StudentMajor.objects.filter(student__user__email__exact=current_user.email)  ##student__user__email
        userint = StudentInterest.objects.filter(student__user__email=current_user.email)
        temp_name = current_user.name.split(" ", 1)
        if temp_name.__len__() == 1:
            last_name = ''
        else:
            last_name = temp_name[1]
        if student:
            formatted_enroll = student.enrollment_date.strftime("%Y-%m-%d")
            formatted_graddate = student.graduation_date.strftime("%Y-%m-%d")
        else:
            formatted_enroll = None
            formatted_graddate = None

        return render(request, "editaccount.html",
                      {"User": current_user, "Stu": student, "MemsInOrg": userInOrgs, "usermajors": userMaj,
                       "userinterest": userint,
                       "interests": allints, "firstname": temp_name[0], "lastname": last_name,
                       "majors": Major.objects.all(), "enrollment_date": formatted_enroll,
                       "graduation_date": formatted_graddate})

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
                actMaj = Major.objects.get(name=remmaj)
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
        current_user = user_util.User_Util.get_user(email=request.session['user'])

        student = user_util.User_Util.get_student(email=current_user.email)
        return render(request, "viewaccount.html",
                      {"message": "user sucessfully edited", "User": current_user, "Stu": student,
                       "MemsInOrg": userInOrgs,
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
        point_of_contacts = User.objects.filter(role__exact=3)
        return render(request, 'createorganization.html',
                      {"user": current_user, "point_of_contacts": point_of_contacts})

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

        return render(request, "createorganization.html.html", {"success_message": "Organization Successfully created"})


class EditOrganization(View):
    def get(self, request):
        cur_user = user_util.User_Util.get_user(request.session['user'])
        org = Organization.objects.get(user=cur_user)
        pocs = User.objects.filter(role=3)
        return render(request, 'editorganization.html', {'user': cur_user, 'organization': org, 'contacts': pocs})

    def post(self, request):
        cur_user = user_util.User_Util.get_user(request.session['user'])
        org = Organization.objects.get(user=cur_user)
        cur_user.password = request.POST.get('password')

        org.point_of_contact = request.POST.get('point_of_contact')
        org.membersCount = request.POST.get('membersCount')
        org.description = request.POST.get('description')

        cur_user.save()
        org.save()
        return render(request, 'editorganization.html', {'user': cur_user, 'organization': org,
                                                         'message': 'Organization information changed successfully!'})


class CreateEvent(View):
    def get(self, request):
        tags = Interest.objects.all()
        current_user = user_util.User_Util.get_user(email=request.session['user'])
        orgs = Organization.objects.filter(user__email__exact=current_user.email)
        search = request.GET.get('search-input', '')
        filtered_interests = Interest.objects.filter(tag__icontains=search)
        return render(request, "createevent.html",
                      {"interests": filtered_interests, "orgs": orgs, "user": current_user, })

    def post(self, request):
        tags = Interest.objects.all()
        current_user = user_util.User_Util.get_user(email=request.session['user'])
        orgs = Organization.objects.filter(user__email__exact=current_user.email)
        search = request.GET.get('search-input', '')
        filtered_interests = Interest.objects.filter(tag__icontains=search)

        name = request.POST.get('name')
        org_name = request.POST.get('org')

        time_happening = request.POST.get('time-happening')
        description = request.POST.get('description')
        time_published = datetime.now()
        loc_check = request.POST.get('SuggestedAdrress')
        photo = request.FILES.get('photo')
        current_user = user_util.User_Util.get_user(email=request.session['user'])
        orgs = Organization.objects.filter(user__email__exact=current_user.email)
        search = request.GET.get('search-input', '')
        filtered_interests = Interest.objects.filter(tag__icontains=search)

        try:
            selected_org = Organization.objects.get(name=org_name)
        except Organization.DoesNotExist:
            return render(request, "createevent.html", {"interests": filtered_interests, "orgs": orgs, "user": current_user,"error_message": "Selected organization does not exist"})

        if loc_check is None or loc_check is '':
            return CreateEvent.get(self,request)

        event = Event.objects.create(name=name, organization=selected_org, loc_addr=request.POST.get('loc_addr'),
                                     loc_city=request.POST.get('loc_city'),
                                     loc_state=request.POST.get('loc_state'),
                                     loc_zip=request.POST.get('loc_zip'),
                                     time_happening=time_happening, description=description,
                                     time_published=time_published, image=photo)
        event.save()

        interests = request.POST.getlist("selected_interests")
        for tag in interests:
            eventTag = EventTag.objects.create(event=event, interest=Interest.objects.get(tag=tag))
            eventTag.save()
            # should not get here
            if isinstance(eventTag, ValueError):
                check = Interest.objects.all()
                return render(request, "createevent.html",
                              {"error_message": 'Search Tag could not be applied', "interests": check})

        return render(request, "createevent.html",
                      {'success_message': 'Event created successfully', "orgs": orgs, "user": current_user,
                       "interests": filtered_interests})


class EditEvent(View):
    def get(self, request, name):
        current_user = user_util.User_Util.get_user(request.session['user'])

        try:
            event = Event.objects.get(name=name)
            time = event.time_happening.strftime("%Y-%m-%dT%H:%M")
            request.session['oldname'] = event.name
            return render(request, "editevent.html", {"event": event, 'time': time})
        except:
            return render(request, "homepage.html", {"error_message": "Event does not exist"})

    def post(self, request, name):
        event = Event.objects.get(name=name)
        event.name = request.POST.get('name')
        # loc = event_util.Event_Util.verify_event_loc(request.POST.get('loc_addr'),
        #                                              request.POST.get('loc_city'),
        #                                              request.POST.get('loc_state'),
        #                                              request.POST.get('loc_zip'))
        # if isinstance(loc, ValueError):
        #     # does this work?
        #     return EditEvent.get(self, request=request, name=event.name)

        event.time_happening = request.POST.get('time_happening')
        event.loc_addr = request.POST.get('loc_addr')
        event.loc_city = request.POST.get('loc_city')
        event.loc_state = request.POST.get('loc_state')
        event.loc_zip = request.POST.get('loc_zip')
        event.description = request.POST.get('description')
        event.image = request.FILES.get('image')

        event.save()

        return render(request, "editevent.html", {'message': 'Event Information Changed Successfully!', 'event': event,
                                                  'time': event.time_happening})


class CalendarView(View):
    def get(self, request):
        return render(request, "calendar.html", {"name": 'publicEvents'})
