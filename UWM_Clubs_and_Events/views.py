from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from UWM_Clubs_and_Events.models import User, Major, Interest, Event
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

        # res = user_util.User_Util.create_user(name= request.POST.get("firstname")+" " + request.POST.get("lastname"), email= request.POST.get("email"), password=request.POST.get("password"),
        #                                           role=0)
        res = user_util.User_Util.create_user(name=firstName + " " + lastName, email=email, password=password,
                                              role=0)
        if isinstance(res, ValueError):
            return render(request, "createaccount.html", {"message": res, "interests": search, "majors": allmajors})

            # this is returning the email not the user object?
        check_user = user_util.User_Util.get_user(email=email)

            # adds every tage fo interest to user

        for tags in interests:
            value = user_util.User_Util.set_user_interest(email=check_user.email, interest=tags)
                #should not get here
            if isinstance(value, ValueError):
                return render(request, "createaccount.html", {"message": res, "interests": search, "majors": allmajors})

        for maj in major:
            print(maj)
            add_major = user_util.User_Util.set_user_major(email=check_user.email, majorname=maj)

            if isinstance(add_major, ValueError):
                return render(request, "createaccount.html", {"message": res, "interests": search, "majors": allmajors})
        return render(request, "login.html", {"success_message": "user account successfully created"})

class Logout(View):
    def get(self, request):
        try:
            logout(request)
        except KeyError:
            pass
        return redirect("login")
    
class ViewEvent(View):
    def get(self, request, name):
        try:
            event = Event.objects.get(name=name)
            return render(request, "viewevent.html", {"Event": event})
        except:
            return render(request, "homepage.html", {"error_message": "Event does not exist"})
        
    