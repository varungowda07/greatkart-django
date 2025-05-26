from django.shortcuts import render, redirect
from .forms import CustomLoginForm, RegisterForm
from django.contrib import messages
from django.contrib.auth import authenticate, logout,login as auth_login
from django.contrib.auth.decorators import login_required


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful. You can now log in.')
            return redirect('login')  # Change to your login URL name
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = CustomLoginForm(request,data=request.POST)
        if form.is_valid():
            user = form.get_user()
            print("DEBUG USER:", user)
            auth_login(request, user)  # ✅ use the aliased function
            return redirect('dashboard')    # make sure 'home' is a valid URL name
        else:
            messages.error(request, 'Invalid username or password')
    else:
        form = CustomLoginForm()
    return render(request, 'accounts/login.html', {'form': form})
def user_logout(request):
    logout(request)
    return redirect('login')


@login_required(redirect_field_name='login')
def dashboard(request):
    return render(request, 'accounts/dashboard.html')
