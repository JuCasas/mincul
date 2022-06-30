from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from authentication.models import User


def signin(request):
    if(request.POST):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print("ESTO!")
            print(user.groups)
            return redirect('listProjects')
        else:
            error_message = "Sus credenciales de inicio de sesión no son correctas. " + \
                            "Si no cuenta con un usuario, comuníquese con el administrador"
            context = {
                'error_message': error_message,
            }
            return render(request, 'authentication/signin.html', context)

    context = {
    }
    return render(request, 'authentication/signin.html', context)

def signout(request):
    logout(request)
    return redirect('signin')