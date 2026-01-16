from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User, Group
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Account created for {user.username}! You are now logged in and assigned to {user.groups.first().name}.')
            return redirect('modules:module_list')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field.capitalize()}: {error}')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('users:profile')
        else:
            for form in [u_form, p_form]:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f'{field.capitalize()}: {error}')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, 'users/profile.html', {'u_form': u_form, 'p_form': p_form})

@staff_member_required
def assign_course(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        course_name = request.POST.get('course')
        try:
            user = User.objects.get(username=username)
            course = Group.objects.get(name=course_name)
            user.groups.set([course])  # Ensure single course
            user.save()
            messages.success(request, f'Assigned {course_name} to {username}.')
            return redirect('users:assign_course')
        except User.DoesNotExist:
            messages.error(request, 'User not found.')
        except Group.DoesNotExist:
            messages.error(request, 'Course not found.')
    users = User.objects.all()
    courses = Group.objects.all()
    return render(request, 'users/assign_course.html', {'users': users, 'courses': courses})