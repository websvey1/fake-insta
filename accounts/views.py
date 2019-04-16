from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login as auth_login, logout as auth_logout, update_session_auth_hash
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .forms import *

# Create your views here.
def signup(request):
    if request.user.is_authenticated:
        return redirect('posts:list') # 로그인 한 상태에서 회원가입 누르면 인덱스로 리턴!!!
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('posts:list')
    else:
        form = UserCreationForm()
    ctx = {
        'form': form,
    }
    return render(request, 'accounts/form.html', ctx) # signup.html로 가도 된다
    
def login(request):
    if request.user.is_authenticated:
        return redirect('posts:list')
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.GET.get('next') or 'posts:list')
    else:
        form = AuthenticationForm()
        next_url = request.GET.get('next', '')
    ctx = {
        'form': form,
        'next': next_url,
    }
    return render(request, 'accounts/form.html', ctx)

@require_POST
@login_required
def logout(request):
    auth_logout(request)
    return redirect('posts:list')

def people(request, username):
    people = get_object_or_404(get_user_model(), username=username)
    context = {
        'people':people,
        }
    return render(request, 'accounts/people.html', context)

@login_required
def edit(request):
    if request.method == 'POST':
        form = UserCustomChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('posts:list')
    else:
        form = UserCustomChangeForm(instance=request.user)
    ctx = {
        'form': form,
    }
    return render(request, 'accounts/form.html', ctx)
    
@require_POST
@login_required
def delete(request):
    user = request.user
    user.delete()
    return redirect('posts:list')

@login_required
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('posts:list')
    else:
        form = PasswordChangeForm(request.user)
    ctx = {
        'form': form,
    }
    return render(request, 'accounts/form.html', ctx)