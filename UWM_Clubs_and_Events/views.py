from django.views.generic import ListView
from django.views import View
from django.shortcuts import render, redirect
from classes import user_util
from .models import User, UserInterest, Interest, Major, UserMajor
from django.db.models import Q


class login(View):
    def get(self, request):
        return render(request, 'login.html', {"name": "login"})

    def post(self, request):
        noSuchUser = False
        badPassword = False
        try:
            email = request.POST['username']
            password = request.POST['password']
            user = User.objects.get(email=request.POST['username'])
            badPassword = (user.password != request.POST['password'])
        except:
            noSuchUser = True
        if email == '' and password == '':
            return render(request, "login.html", {"message": "Nothing entered"})
        elif email == '':
            return render(request, "login.html", {"message": "No email"})
        elif password == '':
            return render(request, "login.html", {"message": "no password"})
        elif noSuchUser:
            return render(request, "login.html", {"message": "no user in database"})
        elif badPassword:
            return render(request, "login.html", {"message": "no user with this password"})
        else:
            return redirect("homepage.html")


class Homepage(View):
    def get(self, request):
        return render(request, "homepage.html", {})


class CreateAccount(View):
    def get(self, request):

        search = request.GET.get('search-input"', '').lower()

        filtered_interests = Interest.objects.filter(tag__icontains=search)

        res_majors = Major.objects.all()
        print(res_majors)

        return render(request, "createaccount.html", {"interests": filtered_interests, "majors": res_majors})

    def post(self, request):
        start_interest = request.GET.get('search-input"', '').lower()
        try:

            firstName = request.POST.get("firstname")
            lastName = request.POST.get("lastname")
            email = firstName = request.POST.get("email")
            password = request.POST.get("password")
            major = request.POST.getlist("major")
            interests = request.POST.getlist("selected_interests")

            res = user_util.User_Util.create_user(name=firstName + " " + lastName, email=email, password=password,
                                                  role=0)
            if not res:
                return render(request, "createaccount.html",
                              {"message": "either incorrect email or blank name", "interests": start_interest})

            # this is returning the email not the user object?
            check_user = User.objects.get(email__iexact=email)

            print(interests)
            # adds every tage fo interest to user
            for tags in interests:
                res = user_util.User_Util.set_user_interest(email=check_user, interest=interest)
                res.save()
        except:
            print("in exception?")
            # this will check fi the email has extact same name (not case sensitive )
            if firstName == '':
                return render(request, "createaccount.html", {"message": "No name inputted"})
            elif lastName == '':
                return render(request, "createaccount.html", {"message": "No last name inputted"})
            elif email == '':
                return render(request, "createaccount.html", {"message": "No email"})
            elif password == '':
                return render(request, "createaccount.html", {"message": "no password"})
        return render(request, "login.html", {"message": "user account successfully created"})
