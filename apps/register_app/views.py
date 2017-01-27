from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User

import re
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your views here.
def index(request):
    # User.objects.all().delete()
    return render(request, "register_app/index.html")

def register(request):
    if request.method == "GET":
        return redirect('/')
    #variables for form information
    fname = request.POST['first_name'].lower()
    lname = request.POST['last_name'].lower()
    email = request.POST['email'].lower()
    password = request.POST['password'].encode()
    confirm_password = request.POST['confirm_password'].encode()
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())

    #registration validaation. try to break the registration process and add more validations
    wrong = False
    if len(fname) < 1:
        wrong = True
        messages.warning(request, "First name cannot be blank!")
    if not fname.isalpha():
        wrong = True
        messages.warning(request, "First name cannot contain numbers!")
    if len(lname) < 1:
        wrong = True
        messages.warning(request, "Last name cannot be blank!")
    if not lname.isalpha():
        wrong = True
        messages.warning(request, "Last name cannot contain numbers!")
    if len(email) < 1:
        wrong = True
        messages.warning(request, "Email cannot be blank!")
    if not EMAIL_REGEX.match(email):
        wrong = True
        messages.warning(request, "Emails are not valid!")
    email_list = User.objects.filter(email=email)
    if email_list:
        wrong = True
        messages.warning(request, "Email is already registered! ")
    if len(password) < 1 or len(password) < 8:
        wrong = True
        messages.warning(request, "Password cannot be blank and atleast 8 characters!")
    if confirm_password != password:
        wrong = True
        messages.warning(request, "Passwords must match!")
    if not password == password:
        wrong = True
        messages.warning(request, "Passwords do not match!")
    if wrong:
        return redirect('/')

    else:
        messages.success(request, "Congratulations you passed the registration process DOOFUS!")
        User.objects.create(first_name=request.POST['first_name'], last_name= request.POST['last_name'], email= request.POST['email'], password= hashed)
        print fname
        print lname
        print email
        print password
        print confirm_password
        print hashed
        return redirect('/')





def login(request):
    print request.POST['user_email']
    user_email=request.POST['user_email']
    print user_email
    email_list = User.objects.filter(email=user_email)
    # password_list = User.objects.filter(password=password)

    hashed = email_list[0].password
    print hashed
    password = request.POST['password']
    if email_list:
        #grabs hashed variable(holding our email_list[0].password) and compares it to the database pw
        if bcrypt.hashpw(password.encode(), hashed.encode()) == hashed.encode():
            request.session['id'] = email_list[0].id
            request.session['first_name'] = email_list[0].first_name
            print "Logged in!"
            return redirect('/success')
        else:
            print "Wrong PW"
            return redirect('/')


def success(request):
    return render(request, "register_app/login.html")


def logout(request):
    if request.method == "GET":
        return redirect('/')
    request.session.pop("id")
    request.session.pop("first_name")
    return redirect('/')
