from django.shortcuts import render

# Create your views here.
from patrimonios.models import Patrimonio


def patrimonio_list(request):

    context = {
        'patrimonios': Patrimonio.objects.all()
    }


    return render(request, 'patrimony/patrimony_list.html',context=context)