from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from users.forms import RegisterForm, ProfileUpdateForm
from django.contrib.auth import authenticate, login, logout
from users.models import Profile
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

# Create your views here.

# Register/Sign Up Page --------------------------
def register(request):

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(
                request,
                'Welcome {}, your account has been scuccessfully created. Now you may login below'.format(username)
            )
            return redirect('users:login')
    else:
        form = RegisterForm()
    
    context = {
        'form':form
    }

    return render(request, 'users/register.html', context)

# Login Page ------------------------------------
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is None:
            messages.error(request, 'Invalid Login. Please try again.')
            return redirect('users:login')

        # For superusers
        elif user.is_superuser:
            login(request, user)
            messages.success(
                request, 
                f'Welcome {user.username}, you are logged in as a SuperUser.'
            )
            return redirect('index')

        # For regular users
        elif user is not None:
            # Ensure user has a profile
            if not hasattr(user, 'profile'):
                Profile.objects.create(user=user)

            login(request, user)
            messages.success(
                request,
                f'Welcome {user.username}, you have been logged in successfully.'
            )
            return redirect('index')

    return render(request, 'users/login.html')

# LogOut Page ----------------------------------------
def logout_view(request):
    if request.method == 'POST':  # Logout only if the user confirms
        user = request.user.username
        logout(request)
        messages.success(request, f'{user}, you have been logged out successfully.')
        return redirect('index')  # Redirect to homepage after logout
    
    return render(request, 'users/logout.html')  # Render the logout confirmation page

# Profile Page ---------------------------------------
@login_required
def profile_page(request):
    profile = get_object_or_404(Profile, user=request.user)
    context = {
        'profile': profile
    }
    return render(request, 'users/profile.html', context)

@login_required
def profform(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('users:profile')
    else:
        form = ProfileUpdateForm(instance=profile)

    context = {
        'form': form
    }
    return render(request, 'users/profform.html', context)