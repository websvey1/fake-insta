from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
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
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)    # 프로필 추가
            auth_login(request, user)
            return redirect('posts:list')
    else:
        form = CustomUserCreationForm()
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
            # return redirect('posts:list')
            return redirect('people', request.user.username)  # 인자가 왜 필요한거지 ? 없어도 될거같은데
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
            update_session_auth_hash(request, user)  # 비번변경시 로그아웃 되지 않게 해주는 것, 인자가 요청과 객체
            return redirect('posts:list')
    else:
        form = PasswordChangeForm(request.user)
    ctx = {
        'form': form,
    }
    return render(request, 'accounts/form.html', ctx)

@login_required
def profile_update(request):
    profile = Profile.objects.get_or_create(user=request.user)  # 카카오로그인으로 하면, 로그인 절차를 무시하고 로그인하기때문에 
                                                                # 프로필을 생성하지 않는다. 따라서 프로필이 있으면 get하고 없으면 create한다
    if request.method=="POST":
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('people', request.user.username)
    else:
        profile_form = ProfileForm(instance=request.user.profile)
    context = {
        'profile_form': profile_form,
    }
    return render(request, 'accounts/profile_update.html', context)
        
@login_required
def follow(request, user_pk):
    people = get_object_or_404(get_user_model(), pk=user_pk)
    if request.user in people.followers.all():
        people.followers.remove(request.user)
    # people(팔로우 누르려고 하는 애)이 팔로우 하고 있는 모든 유저중에, 현재 접속유저가 있으면, 언팔
    else:
        people.followers.add(request.user)
    return redirect('people', people.username)
    # 아니면 팔로우