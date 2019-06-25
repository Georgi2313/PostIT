from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.utils import timezone
from django.http import HttpResponse 
from .models import Posts
from .forms import *


def signup(request):
    form = AccountForm(request.POST)
    if request.method == 'POST' :
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            form= AccountForm()
            return render(request,'webapp/signup.html',{'form' : form})
    else :
        form = AccountForm()
        return render(request,'webapp/signup.html',{'form' : form})

@login_required
def view_profile(request):
    user_info=request.user
    return render(request,'webapp/view_profile.html',{'user_info': user_info})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('view_profile')
    
    else: 
        form = EditProfileForm(instance=request.user)
        return render(request,'webapp/edit_profile.html',{'form':form})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request,form.user)
            return redirect('edit_profile')
        else:
            return redirect('change_password')
    else: 
        form = PasswordChangeForm(user=request.user)
        return render(request,'webapp/change_password.html',{'form':form})


@login_required
def add(request): 
    if request.method == 'POST': 
        form = AddForm(request.POST, request.FILES)   
        if form.is_valid(): 
            post = form.save(commit=False)
            post.author = request.user
            post.created_date = timezone.now()
            post.save() 
            return redirect('success') 
    else: 
        form = AddForm() 
    return render(request, 'webapp/add.html', {'form' : form}) 
  
@login_required  
def success(request): 
    return redirect('/home')

@login_required
def home(request):
    if request.method == 'GET': 
        #posts = Posts.objects.filter(author = request.user).order_by('-post_date')
        posts = Posts.objects.all()
        return render(request,'webapp/home.html',{'posts':posts})



