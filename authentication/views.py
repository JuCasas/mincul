from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from conservacion.models import Actividad


def signin(request):
    if(request.POST):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        print("Hola")
        if user is not None:
            login(request,user)
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

def logout(request):
    # user = User.objects.get(pk=request.user.pk)
    # user.rol_actual = None
    # user.save()
    # logout(request)
    context = {
    }
    return render(request, 'authentication/signin.html', context)