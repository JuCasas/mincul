from django.shortcuts import render

# Create your views here.
from patrimonios.models import Patrimonio


def patrimonio_list(request):

    context = {
        'patrimonios': Patrimonio.objects.all()
    }


    return render(request, 'patrimonio/patrimony_list.html', context=context)

def patrimonio_edit(request,pk):
    patrimonio = -1
    #patrimonio = Patrimonio.objects.get(pk=pk)
    context = {
        'patrimonio': patrimonio,
    }
    return render(request, 'patrimonio/patrimony_inmaterial_edit.html', context)