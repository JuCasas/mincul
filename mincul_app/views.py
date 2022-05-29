from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from patrimonios.models import PatrimonioValoracion
# Create your views here.
def template(request):
    return render(request, 'template_auth.html')

def detalle(request):
    if request.POST:
        print(request.POST)
        valoracion = PatrimonioValoracion.objects.create()
        #falta la conexion con detalle del patrimonio, coordinar con el grupo encargado
        valoracion.nombre = request.POST.get("name")
        valoracion.correo = request.POST.get("email")
        valoracion.comentario = request.POST.get("comment")
        valoracion.valoracion = request.POST.get("score")
        valoracion.save()
        return HttpResponseRedirect(reverse(detalle))
    return render(request, 'templateDetail.html')

def login(request):
    return render(request, 'patrimony/patrimony_list.html')

def material(request):
    return render(request, 'materialKit.html')