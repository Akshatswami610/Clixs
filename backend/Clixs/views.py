from django.shortcuts import render

def login(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'signup.html')

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def addpost(request):
    return render(request, 'addpost.html')

def profile(request):
    return render(request, 'profile.html')

def chat(request):
    return render(request, 'chat.html')

def contactus(request):
    return render(request, 'contactus.html')