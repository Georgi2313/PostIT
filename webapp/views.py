from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from urllib.parse import quote_plus
from django.utils import timezone
from django.http import HttpResponse
from facepy import GraphAPI 
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
def view_post(request,pk):
    if request.method == 'GET':
        post=get_object_or_404(Posts,pk=pk)
#        post = Posts.objects.get(pk=pk)
        if request.user.username == post.author:
            twitter_share_code = quote_plus(post.body)
            return render(request,'webapp/view_post.html',{'post':post,'twitter_share_code':twitter_share_code})
        else:
            return render(request,'webapp/unauthorized_access.html',{})

@login_required
def edit_post(request,pk):   
    if request.method == 'POST':
        post=get_object_or_404(Posts,pk=pk)
        form=AddForm(request.POST,request.FILES,instance=post)
        if form.is_valid():
            post=form.save(commit=False)
            post.save()
            return redirect('/home')
        
    post=get_object_or_404(Posts,pk=pk)
    form=AddForm(instance=post)
    if request.user.username == post.author:
        return render(request,'webapp/edit_post.html',{'form':form}) 
    else:
        return render(request,'webapp/unauthorized_access.html',{})    

@login_required
def delete_post(request,pk):

    post = Posts.objects.get(pk=pk)
    if request.user.username == post.author:
        post = Posts.objects.get(pk=pk).delete()
        return redirect('/home')
    return render(request,'webapp/unauthorized_access.html',{}) 
    

@login_required
def home(request):
    if request.method == 'GET': 
        posts = Posts.objects.filter(author = request.user,post_date__range=[timezone.now(), "2020-01-31"]).order_by('post_date')
#        posts = Posts.objects.all()
        return render(request,'webapp/home.html',{'posts':posts})

@login_required
def past(request):
    if request.method == 'GET': 
        posts = Posts.objects.filter(author = request.user,post_date__range=["2018-01-31",timezone.now()]).order_by('-post_date')
        return render(request,'webapp/home.html',{'posts':posts})

@login_required
def post_to_fb(request):
    oauth_access_token=EAAOyrUXzEuQBADrP5Qsnk9RBPn520wdhJcXFKUU8EqJZBvZA0ylj8Qgc7ZB289N0wKyNo8254toPrB9przZCUJj3feYAthYpPVhrQ78d4qGAowRUZBZCjbSirvjXZC05VJxkBB0OFt5ThcKLU57o8XIQgGWSz4W5CC7FrkCkOQ7yP25iYPckMlR0S9DzMIaiI4ZD
    graph=GraphAPI(oauth_access_token)
    #graph.post(path="me/feed", message="hello FB", caption="hello FB", description="hello FB")
    graph.post(
        path = 'me/photos',
        source = open('postit.pythonanywhere.com/media/images/1561900a440900282329821236643243.jpg', 'rb')
    )
    return render(request,'webapp/home.html',{})

