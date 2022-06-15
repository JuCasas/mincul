from django.core import serializers
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.
from authentication.models import User
from patrimonios.models import Patrimonio, Institucion
from patrimonios.serializers import InstitucionSerializer, UserSerializer


def patrimonio_list(request):

    context = {
        'patrimonios': Patrimonio.objects.all()
    }


    return render(request, 'patrimonio/patrimony_list.html', context=context)

@api_view(('GET',))
def instituciones_list_api(request):
    length = 10
    search = request.GET['search']
    page = int(request.GET['page'][0])
    start = (page - 1) * length
    end = start + length
    queryset = Institucion.objects.filter(nombre__icontains=search,estado='1').order_by('nombre')
    count = queryset.count()
    queryset = queryset[start:end]
    serializer = InstitucionSerializer(queryset, many=True)
    result = dict()
    result['items'] = serializer.data
    result['total_count'] = count
    return Response(result, status=status.HTTP_200_OK, template_name=None, content_type=None)

@api_view(('GET',))
def gestorPatrimonio_list_api(request):
    length = 10
    search = request.GET['search']
    page = int(request.GET['page'][0])
    start = (page - 1) * length
    end = start + length
    queryset = User.objects.filter(first_name__icontains=search).order_by('first_name')
    count = queryset.count()
    queryset = queryset[start:end]
    serializer = UserSerializer(queryset, many=True)
    result = dict()
    result['items'] = serializer.data
    result['total_count'] = count
    return Response(result, status=status.HTTP_200_OK, template_name=None, content_type=None)

def patrimonio_edit(request,pk):
    patrimonio = -1
    #patrimonio = Patrimonio.objects.get(pk=pk)
    context = {
        'patrimonio': patrimonio,
    }
    if int(pk) == 1:
        return render(request, 'patrimonio/patrimony_inmueble_edit.html', context)
    else:
        return render(request, 'patrimonio/patrimony_inmaterial_edit.html', context)
