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
            roles = list(user.groups.values_list())
            if (len(roles)==1):
                if(roles[0][1] == 'Gestor de Conservación y Traslados' or roles[0][1] =='Conservador'):
                    return redirect('listProjects')
                elif(roles[0][1] == 'Gestor de Patrimonios'):
                    return redirect('patrimonio_list')
            else:
                error_message = "ERROR"
                context = {
                    'error_message': error_message,
                }
                return render(request, 'authentication/signin.html', context)
        else:
            error_message = "ERROR"
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