from django.views import View
from django.shortcuts import render, redirect
from .models import User, UserInterest, Interest, Major


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
        userint = request.GET.get(substring ="sear_bar")
        interests = Interest.objects.filter()
        majors = Major.objects.all()
        return render(request, "createaccount.html", {"interests": interests, "major": majors})

    def post(self, request):
        try:

            firstName=request.POST['firstname']
            lastName = request.POST['lastname']
            email = firstName=request.POST['email']
            password = request.POST['password']
            major = request.POST['major']
            interest = request.kwargs['search_bar']
            newUser = User(name=firstName,lastName=password, email=email
                           , password=password, major=major, interest=interest)


        except:
            if(User.objects.filter(email__iexact=email)):
                return render(request, "createaccount.html", {"message": "user with email exists "})
            elif firstName == '':
                return render(request, "createaccount.html", {"message": "No name inputted"})
            elif lastName == '':
                return render(request, "createaccount.html", {"message": "No last name inputted"})
            elif email == '':
                return render(request, "createaccount.html", {"message": "No email"})
            elif password == '':
                return render(request, "createaccount.html", {"message": "no password"})






