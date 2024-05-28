from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.contrib import auth
from datetime import datetime
import time
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse

class AutoLogoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == reverse('login') and request.user.is_authenticated:
            # If the user is already authenticated and trying to access the login page,
            # log them out and redirect to the login page
            auth.logout(request)
            return HttpResponseRedirect(reverse('login'))
        response = self.get_response(request)
        if request.user.is_authenticated:
            last_activity_str = request.session.get('last_activity')
            if last_activity_str:
                last_activity = datetime.fromisoformat(last_activity_str)
                idle_duration = timezone.now() - last_activity
                print(f"Middleware: Idle duration: {idle_duration.total_seconds()} seconds")
                if idle_duration.total_seconds() > 900:  # Adjust the idle duration as needed
                    return HttpResponseRedirect(reverse('logout'))  # Redirect to logout view URL
            else:
                print("Middleware: 'last_activity' key not found in session")
                request.session['last_activity'] = str(timezone.now())  # Set 'last_activity' if not exists
                print("Middleware: 'last_activity' key set in session")
        else:
            print("Middleware: User not authenticated")
        return response

class LoginAttemptMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
 
    def __call__(self, request):
        if request.method == 'POST' and request.path == reverse('login'):  # Assuming your login URL name is 'login'
            username = request.POST.get('username')
            now = time.time()
            last_attempt_time = request.session.get(f'{username}_last_attempt_time', 0)
 
            # Check if login attempts exceed the limit
            if request.session.get(f'{username}_attempts', 0) >= settings.MAX_LOGIN_ATTEMPTS:
                if now - last_attempt_time < settings.LOGIN_ATTEMPT_COOLDOWN:
                    remaining_time = int(settings.LOGIN_ATTEMPT_COOLDOWN - (now - last_attempt_time))
                    messages.error(request, f"Too many login attempts. Please try again after {remaining_time // 60} minutes.")
                    return redirect(reverse('login'))  # Redirect to login page
 
            # If login attempt is successful, reset the attempt count and last attempt time
            # You may want to replace this with your actual authentication logic
            if login_successful(request.POST.get('username'), request.POST.get('password')):
                request.session[f'{username}_attempts'] = 0
                request.session[f'{username}_last_attempt_time'] = 0
            else:
                # Increment the login attempt count and update the last attempt time
                request.session[f'{username}_attempts'] = request.session.get(f'{username}_attempts', 0) + 1
                request.session[f'{username}_last_attempt_time'] = now
 
                if request.session[f'{username}_attempts'] >= settings.MAX_LOGIN_ATTEMPTS:
                    # If max attempts reached, set the last attempt time to enforce cooldown
                    request.session[f'{username}_last_attempt_time'] = now
 
        response = self.get_response(request)
        return response
 
def login_successful(username, password):
    # Implement your actual authentication logic here
    # Return True if the login is successful, False otherwise
    return False  # Placeholder, replace with your actual authentication logic