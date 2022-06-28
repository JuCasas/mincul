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
    actividad = Actividad.objects.get(pk=1)
    conservadores = actividad.conservadores.all()

    context = {
        'activity': actividad,
        'conservadores': conservadores
    }
    return render(request, 'authentication/login.html', context)