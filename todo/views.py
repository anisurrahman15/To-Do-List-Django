from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm
from .models import Todo
from django.utils import timezone
from django.contrib.auth.decorators import login_required


# Create your views here.
def signupuser(request):
    if not request.user.is_authenticated:
        if request.method == 'GET':
            # When someone visits the signup page.
            return render(request, "todo/signupuser.html", {'form': UserCreationForm})
        else:
            # When Someone submit the information.
            if request.POST['password1'] == request.POST['password2']:
                try:
                    user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                    user.save()
                    login(request, user)
                    return redirect('currenttodos')  # Return redirect returns "Url" from name created in url.py
                except IntegrityError:  # integrity error happens when one username matched with another existing username.
                    return render(request, "todo/signupuser.html",
                                  {'form': UserCreationForm,
                                   'error': 'Username is already been taken. Please choose a new username'})

            else:
                # Tell the user the passwords didn't match.
                return render(request, "todo/signupuser.html",
                              {'form': UserCreationForm, 'error': 'Passwords did not match'})
    else:
        return render(request, "todo/AuthResponse.html")

def loginuser(request):
    if not request.user.is_authenticated:
        if request.method == 'GET':
            # When someone visits the signup page.
            return render(request, "todo/loginuser.html", {'form': AuthenticationForm()})
        else:
            user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
            if user is None:
                return render(request, "todo/loginuser.html",
                              {'form': AuthenticationForm(), 'error': 'Username or Password Does not exist'})
            else:
                login(request, user)
                return redirect('currenttodos')
    else:
        return render(request, "todo/AuthResponse.html")


@login_required
def currenttodos(request):
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=True)
    # This line "objects,filter() "filters the objects in database for a specific user and stores it.
    # datecompleted__isnull is checking if datacomplete boolean is null or not.
    # This is way of django to check boolean.
    return render(request, 'todo/currenttodos.html', {'todos': todos})


@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


def home(request):
    return render(request, "todo/home.html")


@login_required
def createtodo(request):
    if request.method == 'GET':
        return render(request, "todo/Createtodo.html", {'form': TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, "todo/Createtodo.html",
                          {'form': TodoForm(), 'error': 'Bad Data Passed in. Try again'})


@login_required
def viewtodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'GET':
        form = TodoForm(instance=todo)
        return render(request, 'todo/viewtodo.html', {'todo': todo, 'form': form})
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/viewtodo.html', {'todo': todo, 'form': form, 'error': 'Bad info'})


@login_required
def completodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.datecompleted = timezone.now()
        todo.save()
        return redirect('currenttodos')


@login_required
def deletetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('currenttodos')


@login_required
def completedtodos(request):
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'todo/completedtodos.html', {'todos': todos})
