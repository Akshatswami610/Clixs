from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db import IntegrityError

User = get_user_model()

# =========================
# Pages
# =========================
def home(request):
    return render(request, "home.html")

def about(request):
    return render(request, "about.html")

def profile(request):
    return render(request, "profile.html")

def addpost(request):
    if request.method == "POST":
        messages.success(request, "Post added successfully!")
        return redirect("home")
    return render(request, "addpost.html")

def chats(request):
    return render(request, "chats.html")

def contactus(request):
    if request.method == "POST":
        messages.success(request, "Message sent successfully!")
        return redirect("contactus")
    return render(request, "contact.html")

def itemdetail(request):
    return render(request, "item-detail.html")

def terms(request):
    return render(request, "terms.html")

def privacy(request):
    return render(request, "privacy.html")

# =========================
# Authentication
# =========================
def login_view(request):
    if request.method == "POST":
        phone_number = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            phone_number=phone_number,
            password=password
        )

        if user:
            auth_login(request, user)
            return redirect("home")

        messages.error(request, "Invalid phone number or password")

    return render(request, "login.html")


def signup_view(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        phone_number = request.POST.get("phone")
        registration_number = request.POST.get("registration_number")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect("signup")

        try:
            User.objects.create_user(
                phone_number=phone_number,
                password=password,
                first_name=first_name,
                last_name=last_name,
                registration_number=registration_number,
            )
            messages.success(request, "Account created successfully!")
            return redirect("login")

        except IntegrityError:
            messages.error(request, "User already exists")
            return redirect("signup")

    return render(request, "signup.html")
