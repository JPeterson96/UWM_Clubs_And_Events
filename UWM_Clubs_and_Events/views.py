from django.views.generic import ListView
from django.views import View
from django.shortcuts import render, redirect
from .models import User, UserInterest, Interest, Major
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

        filter_value = request.GET.get('search-input"', '').lower()

        filtered_interests = Interest.objects.filter(tag__icontains=filter_value)
        print(filtered_interests)


        return render(request, "createaccount.html", {"interests": filtered_interests})

    def post(self, request):
        try:
            firstName = request.POST.get("firstname")
            lastName = request.POST.get("lastname")
            email = firstName = request.POST.get("email")
            password = request.POST.get("password")
            major = request.POST.getlist("major")
            interests = request.POST.get("selected_interests")
            values = request.POST.get("interest_search")
            print(firstName, lastName, email, password, major, interests)
            for v in values:
                interests.append(v)

            # initialize user
            newuser=User.objects.create(name=firstName, lastName=password, email=email
                                , password=password, major=major, interest=interests)
            newuser.save()
            # adds every tage fo interest to user
            for tags in interests:
                res =UserInterest.objects.create(user=newuser, type=tags)
                res.save()
        except:
            # this will check fi the email has extact same name (not case sensitive )
            if (User.objects.filter(email__iexact=email)):
                return render(request, "createaccount.html", {"message": "user with email exists "})
            elif firstName == '':
                return render(request, "createaccount.html", {"message": "No name inputted"})
            elif lastName == '':
                return render(request, "createaccount.html", {"message": "No last name inputted"})
            elif email == '':
                return render(request, "createaccount.html", {"message": "No email"})
            elif password == '':
                return render(request, "createaccount.html", {"message": "no password"})
        return render(request, "login.html", {"message": "user account successfully created"})
