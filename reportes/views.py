from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.db.models.functions import ExtractMonth, ExtractYear
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect

# Create your views here.
from incidente.models import Incidente
from patrimonios.models import Patrimonio, PuntoGeografico

@login_required(login_url='/auth/login/')
def reportes(request):
    return render(request, 'reportes/reportes_gestor.html')

def traerData(request):
    p = PuntoGeografico.objects.annotate(num_incidentes=Count('incidente')).order_by('-num_incidentes')[:5]
    result = p.values_list('num_incidentes', 'nombre')
    print("==========================================")
    print("RESULT")
    print(result)
    print("==========================================")
    numeros = []
    etiquetas = []
    for tuple in result:
        if (tuple[0]!=0):
            print(tuple)
            numeros.append(tuple[0])
            etiquetas.append(tuple[1])

    print("ETIQUETAS")
    print(etiquetas)
    return JsonResponse({"data": numeros, "labels":etiquetas}, status=200)

def traerData2(request):
    result = Incidente.objects.annotate(month=ExtractMonth('fechaOcurrencia'),
                             year=ExtractYear('fechaOcurrencia'),
                               ).order_by().values('month').annotate(total=Count('*')).values('month', 'total')

    print(result)
    numeros = ['0']*12
    for i in range(0,result.count()):
        posicion = (result[i]['month']+4)%12
        numeros[posicion] = result[i]['total']
            # etiquetas.append(result[i][1])

    # return JsonResponse({"data": numeros, "labels":etiquetas}, status=200)
    return JsonResponse({"data": numeros}, status=200)

