
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
        value = request.GET.get('interest_search', '')
        intRes = Interest.objects.filter(tag__icontains=value)
        interests = list(intRes.values_list('tag', flat=True))
        return render(request, "createaccount.html", {"interests": interests})

    def post(self, request):
        try:
            firstName=request.POST.get("firstname")
            lastName = request.POST.get("lastname")
            email = firstName=request.POST.get("email")
            password = request.POST.get("password")
            major = request.POST.get("major")
            interest = request.POST.get("interest_search")
            #initialize user
            newUser = User(name=firstName,lastName=password, email=email
                           , password=password, major=major, interest=interest)
            #adds every tage fo interest to user
            for tags in interest:
                UserInterest(user=newUser.email, type=tags)
        except:
            #this will check fi the email has extact same name (not case sensitive )
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
        return render(request, "login.html", {"message": "user account successfully created"})





