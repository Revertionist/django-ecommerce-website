from django.shortcuts import render
from django.contrib.auth import login, authenticate
from .forms import RegisterForm
# Create your views here.
def signup(request):
    if request.method=="POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = RegisterForm()
    return render (request, 'register/pages/signup.html', {"form": form})