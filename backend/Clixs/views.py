from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from django.contrib.auth import get_user_model
User = get_user_model()


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
        phone_number = request.POST.get("username")  # reuse input field
        password = request.POST.get("password")

        user = authenticate(
            request,
            phone_number=phone_number,
            password=password
        )

        if user is not None:
            auth_login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid phone number or password")

    return render(request, "login.html")


def signup(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        phone_number = request.POST.get("phone")
        reg_no = request.POST.get("registration_number")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect("signup")

        if User.objects.filter(phone_number=phone_number).exists():
            messages.error(request, "Phone number already registered")
            return redirect("signup")

        user = User.objects.create_user(
            phone_number=phone_number,
            password=password,
            first_name=first_name,
            last_name=last_name,
            reg_no=reg_no,
        )

        messages.success(request, "Account created successfully")
        return redirect("login")

    return render(request, "signup.html")
