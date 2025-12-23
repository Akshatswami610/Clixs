from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.models import User
from django.contrib import messages


# =========================
# Pages
# =========================

def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


def profile(request):
    return render(request, 'profile.html')


def addpost(request):
    if request.method == "POST":
        # handle post creation logic here
        messages.success(request, "Post added successfully!")
        return redirect('home')
    return render(request, 'addpost.html')


def chat(request):
    return render(request, 'chat.html')


def contactus(request):
    if request.method == "POST":
        # handle contact form submission here
        messages.success(request, "Message sent successfully!")
        return redirect('contactus')
    return render(request, 'contact.html')


# =========================
# Authentication
# =========================

def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'login.html')


def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('signup')
            return redirect('signup')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        user.save()

        messages.success(request, "Account created successfully")
        return redirect('login')

    return render(request, 'signup.html')
