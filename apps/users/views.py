from re import template
import re
from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages



# Create your views here.
def reg_login(request):
    return render(request, 'reg_login.html')

def new_user(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for error in errors:
            messages.error(request, error)
        return redirect('/')
    request.session['user_id'] =  User.objects.create_user(request.POST)
    return redirect('/')

def login(request):
    valid, result = User.objects.login(request.POST)
    if not valid:
        messages.error(request, result)
        return redirect('/')
    else:
        request.session['user_id'] = result.id
    return redirect('/books')

def logout(request):
    request.session.clear()
    return redirect ('/')

def user_page(request, user_id):
    if 'user_id' not in request.session:
        return redirect('/')
    loged_in_user = User.objects.get(id= request.session['user_id'])
    context = {
        'user': User.objects.get(id = user_id),
        'loged_in_user' : loged_in_user
    }
    user = User.objects.get(id = request.session['user_id'])
    print(user.book_reviews.all())
    return render(request, 'user_page.html', context)
