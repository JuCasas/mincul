from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from conservacion.models import Actividad


def login(request):
    if(request.POST):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('addTaskView',1)
        else:
            error_message = "Sus credenciales de inicio de sesión no son correctas. " + \
                            "Si no cuenta con un usuario, comuníquese con el administrador"
            context = {
                'error_message': error_message,
            }
            return render(request, 'authentication/login.html', context)

    context = {
    }
    return render(request, 'authentication/login.html', context)