from django.shortcuts import render, HttpResponseRedirect, redirect, reverse
from .forms import RegisterForm, LogInForm, ProfileForm, ChangePasswordForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib.auth import decorators


def signUp(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('')
    form = RegisterForm()
    if request.POST:
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            new_user = User(username=username, email=email)
            new_user.set_password(password)
            new_user.save()
            return redirect(reverse('login'))
    context = {"form": form}
    return render(request, 'signup.html', context)


def LogIn(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
    form = LogInForm()
    if request.POST:
        form = LogInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            user = User.objects.get(username=username)
            login(request, user)
            return HttpResponseRedirect('/')
    return render(request, 'login.html', {"form": form})


def logOut(request):
    logout(request)
    return redirect(reverse('login'))


@decorators.login_required
def userProfile(request):
    user = request.user
    data = {"username": user.username, "email": user.email,
            "first_name": user.first_name, "last_name": user.last_name}
    form = ProfileForm(initial=data, instance=user.profile)
    if request.POST:
        form = ProfileForm(request.POST, request.FILES, instance=user.profile)
        if form.is_valid():
            form.save()
            user.username = form.cleaned_data["username"]
            user.email = form.cleaned_data["email"]
            user.first_name = form.cleaned_data["first_name"]
            user.last_name = form.cleaned_data["last_name"]
            user.save()
            return HttpResponseRedirect("/")
    return render(request, 'profile.html', {"form": form})


@decorators.login_required
def changePassword(request):
    form = ChangePasswordForm()
    if request.POST:
        form = ChangePasswordForm(request.POST)
        form.set_user(user=request.user)
        if form.is_valid():
            user = request.user
            user.set_password(form.cleaned_data["new"])
            user.save()
            return HttpResponseRedirect("/")
    return render(request, 'change_password.html', {"form": form})
