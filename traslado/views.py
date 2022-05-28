import datetime

from django.shortcuts import render



def addTransfer(request):
    if request.POST:
        print("Hola")
    else:
        return render(request,'traslado/transfer_add.html')