from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.urls import reverse

from the_people.models import UserManager, User
from the_people.forms import UserCreationForm


def signup(request):
    if request.method == "GET":
        return render(request, "signup.html", {"form": UserCreationForm})

    form = UserCreationForm(request.POST)
    if not form.is_valid():
        return render(request, "signup.html", {"form": UserCreationForm, "errors": form.errors})

    form.save(commit=False)
    
    username = form.cleaned_data.get('username')
    password = form.cleaned_data.get('password1')

    user = authenticate(username=username, password=password)
    if not user:
        user = UserManager.get_UserManager().create_user(username, password)

    user.save()
    login(request, user)
    
    return redirect(reverse('news_page'))
