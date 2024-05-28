from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib import messages
from datetime import datetime, time
 
from django.utils import timezone
from datetime import timedelta
 
def login(request):
    context = {}  # Initialize the context dictionary
   
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
       
        user = None  # Initialize the user variable
       
        # Try to authenticate the user with the provided credentials
        if User.objects.filter(username=username).exists():
            user = auth.authenticate(username=username, password=password)
        else:
            user = User.objects.filter(email=username).first()
            if user:
                user = auth.authenticate(username=user.username, password=password)
       
        if user is not None:
            auth.login(request, user)      
 
            return redirect('index')  # Default redirection if user doesn't have specific role
 
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')  # Redirect back to the login page    
    return render(request, "Login/index.html", context)
 
def logout(request):
    auth.logout(request)
    return redirect('login')  # Replace 'login' with the URL name of your login page