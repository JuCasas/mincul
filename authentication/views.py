from email import message
from multiprocessing import context
from django.http import HttpResponseRedirect

from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import login,logout
# Create your views here.

import requests
from django.views.generic import CreateView

from authentication.forms import UserRegisterForm


class RenderLogin(CreateView):
    # template_name = 'authentication/login.html'

    def get_context_data(self, **kwargs):
        context = {

        }
        return context

def registe(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            messages.success(request,f'Usuario {username} creado')
            return redirect('login')
            
    else:
        form = UserRegisterForm()
            
    context = { 'form':form }
    return render(request,"register.html",context)

def logoutUsuario(request):
    logout(request)
    return redirect('login2')

def EditarCuenta(request):
    