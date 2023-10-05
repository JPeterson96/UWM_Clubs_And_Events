from django.views import View
from django.shortcuts import render, redirect
from .models import User, Major, Interest, UserInterest
from classes import user_util



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


        search = request.GET.get('search-input', '')
        filtered_interests = Interest.objects.filter(tag__icontains=search)
        majors = Major.objects.all()
        return render(request, "createaccount.html", {"interests": filtered_interests, "majors": majors})

    def post(self, request):
        try:
            firstName = request.POST.get("firstname")
            lastName = request.POST.get("lastname")
            email = firstName = request.POST.get("email")
            password = request.POST.get("password")
            major = request.POST.getlist("major")
            interests = request.POST.getlist("selected_interests")

            res = user_util.User_Util.create_user(name= request.POST.get("firstname")+" " + request.POST.get("lastname"), email= request.POST.get("email"), password=request.POST.get("password"),
                                                  role=0)
            if isinstance(res, ValueError):
                return render(request, "createaccount.html", {"message": res})

            # this is returning the email not the user object?
            check_user = user_util.User_Util.get_user(email=email)
            print(check_user.email)


            print(interests)
            # adds every tage fo interest to user
            for tags in interests:
                value = user_util.User_Util.set_user_interest(email=check_user.email, interest=tags)
                #should not get here
                if isinstance(value, ValueError):
                    return render(request, "createaccount.html", {"message": res})
                value.save()
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