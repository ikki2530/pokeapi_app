from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.
from .decorators import unauthenticated_user
from .forms import CreateUserForm

@login_required(login_url='login')
def index(request):
    """
    Página principal
    """
    context = {}
    return render(request, './index.html', context)


@unauthenticated_user
def registerPage(request):
    """
    Registrar nuevos usuarios
    """
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            print("valido!!!")
            user = form.save() # signal se llama después de esto
            print("user", user)
            username = form.cleaned_data.get('username')
            messages.success(request, 'Cuenta creada para ' + username)
            return redirect('login')
    context = {'form': form}
    return render(request, './register.html', context)




@unauthenticated_user
def loginPage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, "Usuario o contraseña incorrecta")
    context = {}
    return render(request, './login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')
