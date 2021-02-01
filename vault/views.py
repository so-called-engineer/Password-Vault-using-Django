from django.shortcuts import render,redirect,get_object_or_404
from django.db import IntegrityError
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from .models import Passwords

def home(request):
    return render(request,'vault_home/home.html')

def loginuser(request):
    if request.method == 'GET':
        return render(request,'vault_home/login.html',{'form':AuthenticationForm()})
    else:
        user = authenticate(request,username=request.POST['username'],password=request.POST['password'])
        if user is None:
            return render(request,'vault_home/login.html',{'form':AuthenticationForm(),'error':'Please check your credentials'})
        else:
            login(request,user)
            return redirect('home')

def signup(request):
    if request.method == 'GET':
        return render(request,'vault_home/signup.html',{'form':UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user=User.objects.create_user(request.POST['username'],password=request.POST['password1'])
                user.save()
                login(request,user)
                return redirect('home')
            except IntegrityError:
                return render(request,'vault_home/signup.html',{'form':UserCreationForm(),'error':'User creation failed. please try again.'})
        else:
            return render(request,'vault_home/signup.html',{'form':UserCreationForm(),'error':'Password didnot match'})

@login_required
def create(request):
    if request.method == "GET":
        return render(request,'vault_home/create.html')
    else:
        if request.POST['password1'] == request.POST['password2'] and request.POST['password1']!='' and request.POST['password2']!='':
            try:
                # Perform your own password encryption mechanism
                # I havent wrote down the logic here implement your own ;-)
                form = Passwords.objects.create(site=request.POST['site'],password=request.POST['password1']),user=request.user)
                form.save()
                return redirect('home')
            except ValueError:
                return render(request,'vault_home/create.html',{'error':'Please enter the data correctly'})
        else:
            return render(request,'vault_home/create.html',{'error':'Please enter the data correctly'})

@login_required
def logoutuser(request):
    if request.method=='POST':
        logout(request)
        return redirect('home')

@login_required
def viewpasswords(request):
    passwords=Passwords.objects.filter(user=request.user)
    return render(request,'vault_home/viewpasswords.html',{'passwords':passwords})

@login_required
def viewpass(request,id):
    password=get_object_or_404(Passwords,pk=id,user=request.user)
    # implement your own logic for decrypting the passwords from the database.
    # realpass= decrypted password.
    return render(request,'vault_home/viewpass.html',{'password':password,'realpass':realpass})

@login_required
def deletepass(request,id):
    password=get_object_or_404(Passwords,pk=id,user=request.user)
    password.delete()
    return redirect('viewpasswords')
