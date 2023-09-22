from django.views import View
from django.shortcuts import render, redirect
from .models import User

class login(View):
    def get(self, request):
        user = User.objects.create(email="test@uwm.edu", password="pass", name="Foo Bar")
        user.save()
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
        elif user == '':
            return render(request, "login.html", {})
        elif password == '':
            return render(request, "login.html", {})
        elif noSuchUser:
            return render(request, "login.html", {})
        elif badPassword:
            return render(request, "login.html", {})
        else:
            return redirect("/homepage/")

class Homepage(View):
    def get(self, request):
        return render(request, "homepage.html", {})