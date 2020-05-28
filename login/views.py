from django.shortcuts import render, redirect
from django.contrib import messages
from . models import User
import bcrypt


def index(request):
    return render(request, "login.html")

def registration_form(request):
    errors =  User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            username = request.POST['username'],
            password = pw_hash
        )
        messages.error(request, "Created Account, please log in")
        return redirect('/')

def login(request):
    users = User.objects.filter(username = request.POST['username'])
    if len(users) != 1:
        messages.error(request, "No user with given username in database")
        return redirect('/')

    user = users[0]

    if not bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
        messages.error(request, "Password does not match")
        return redirect('/')

    request.session['user_id'] = user.id
    request.session['user_username'] = user.username
    request.session['user_email'] = user.email
    return redirect('/success')

def success(request):
    
    if not 'user_id' in request.session:
        messages.error(request, 'Please log in to view this page')
        return redirect('/')

    return render(request, 'success.html')

def logout (request):
    del request.session['user_id']
    del request.session['user_username']
    del request.session['user_email']

    return redirect('/')
