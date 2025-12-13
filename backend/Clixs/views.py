from django.shortcuts import render

def login(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'signup.html')

def home(request):
    return render(request, 'home.html')

def browse(request):
    return render(request, 'browse.html')

def post(request):
    return render(request, 'post.html')

def profile(request):
    return render(request, 'profile.html')

def chat(request):
    return render(request, 'chat.html')

def contactus(request):
    return render(request, 'contactus.html')