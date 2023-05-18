from django.shortcuts import render,redirect 
from django.contrib.auth import authenticate,login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

from accounts.forms import RegistrationUserForm

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("dashboard:index")
        else: 
            messages.warning(request, ("Errore di login - Riprova nuovamente."))
            return redirect("accounts:login")
    else:  
        return render(request, 'authenticate/login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, ("Logout effettuato correttamente."))
    return redirect("accounts:login")

def signup_user(request):
    if request.method == "POST":
        form = RegistrationUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate (username=username, password=password)
            login(request, user)
            messages.success(request, ("Registrazione effettuata correttamente."))
            return redirect("dashboard:index")
    else:  
        form = RegistrationUserForm(request.POST or None)
    
    return render(request, 'authenticate/signup_user.html', {'form':form})