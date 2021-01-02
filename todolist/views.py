from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login as loginUser, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required

from .forms import TaskForm
from .models import Task

# Create your views here.


@login_required(login_url='login')
def index(request):
    if request.user.is_authenticated:
        user = request.user
        form = TaskForm()
        tasks = Task.objects.filter(user = user)
        return render(request, 'index.html', context={'task_form': form, 'tasks': tasks})


def login(request):
    if request.method == 'GET':
        form = AuthenticationForm()
        context = {
            'form': form
        }
        return render(request, 'login.html', context=context)
    else:
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                loginUser(request, user)
                return redirect('index')
        else:
            context = {
            'form': form
            }
            return render(request, 'login.html', context=context)


def signup(request):
    if request.method == 'GET':
        form = UserCreationForm()
        context = {
            'form': form
        }
        return render(request, 'signup.html', context=context)
    else:
        form = UserCreationForm(request.POST)
        context = {
            'form': form
        }
        if form.is_valid():
            user = form.save()
            if user is not None:
                return redirect('login')
        else:
            return render(request, 'signup.html', context=context)

@login_required(login_url='login')
def add_task(request):
    if request.user.is_authenticated:
        user = request.user
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = user
            task.save()
            return redirect('index')
        else:
            return render(request, 'add_task.html', context={'form': form})

# @login_required(login_url='login')
# def index(request):
#     # return HttpResponse("Hello World!!")
#     form = TaskForm()

#     if request.method == "POST":
#         # Get the posted form
#         form = TaskForm(request.POST)
#         if form.is_valid():
#             form.save()
#         return redirect("index")

#     tasks = Task.objects.all() # add this
#     return render(request, "index.html", {"task_form": form, "tasks": tasks})

def update_task(request, pk):
    task = Task.objects.get(id=pk)

    form = TaskForm(instance=task)

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        # print(form)
        # print(form.is_valid())
        if form.is_valid():
            form.save()
            return redirect("index")

    return render(request, "update_task.html", {"task_edit_form": form})

def delete_task(request, pk):
    task = Task.objects.get(id=pk)
    task.delete()
    return redirect("index")



def signout(request):
    logout(request)
    return redirect('login')


