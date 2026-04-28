# views.py

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import TODOO

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def signup(request):
    if request.method == 'POST':
        fnm = request.POST.get('fnm')
        email = request.POST.get('email')
        pwd = request.POST.get('pwd')

        if not fnm:
            return render(request, 'signup.html', {'error': 'Username is required'})

        User.objects.create_user(username=fnm, email=email, password=pwd)
        return redirect('/loginn')

    return render(request, 'signup.html')


def loginn(request):
    if request.method == 'POST':
        fnm = request.POST.get('fnm')
        pwd = request.POST.get('pwd')

        userr = authenticate(request, username=fnm, password=pwd)

        if userr is not None:
            login(request, userr)
            return redirect('/todopage')

        return redirect('/loginn')

    return render(request, 'loginn.html')


@login_required
def todo(request):
    if request.method == 'POST':
        title = request.POST.get('title')

        if title:
            TODOO.objects.create(title=title, user=request.user)

        return redirect('/todopage')

    res = TODOO.objects.filter(user=request.user).order_by('-date')
    return render(request, 'todo.html', {'res': res})


# edit function
@login_required
def edit_todo(request, srno):
    obj = TODOO.objects.get(srno=srno, user=request.user)

    if request.method == 'POST':
        title = request.POST.get('title')
        print(title)

        obj.title = title
        obj.save()

        return redirect('/todopage')

    return render(request, 'edit.html', {'todo': obj})


# delete function
@login_required
def delete_todo(request, srno):
    obj = TODOO.objects.get(srno=srno, user=request.user)
    obj.delete()
    return redirect('/todopage')


# logout function
@login_required
def logoutt(request):
    logout(request)
    return redirect('/loginn')