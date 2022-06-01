from django.shortcuts import render

from patrimonios.models import Servicio
from patrimonios.models import Entrada
from patrimonios.models import ActividadTuristica
from patrimonios.models import Patrimonio
from patrimonios.models import PatrimonioMaterial
from patrimonios.models import PatrimonioMaterialMueble

# Create your views here.

def mapaficha(request):
    patrimonies = Patrimonio.objects.filter(tituloDemoninacion='La Ciudad Sagrada Caral')
    patrimony = patrimonies.first()
    materialPatrimonies = PatrimonioMaterial.objects.filter(patrimonio__tituloDemoninacion='La Ciudad Sagrada Caral')
    materialPatrimony = materialPatrimonies.first()
    activities = ActividadTuristica.objects.filter(patrimoniomaterial__patrimonio_id=patrimony.id)
    if len(activities) >1:
        activities1 = activities[:len(activities) // 2]
        activities2 = activities[len(activities) // 2:]
        if len(activities2) > len(activities1):
            activities2.reverse()
            activities1.append(activities2.pop())
            activities2.reverse()
    else:
        activities1 = activities
        activities2 = []
    tickets = Entrada.objects.filter(patrimoniomaterial__patrimonio_id=patrimony.id)
    services = Servicio.objects.filter(patrimoniomaterial__patrimonio_id=patrimony.id)
    if len(services) >1:
        services1 = services[:len(services) // 2]
        services2 = services[len(services) // 2:]
        if len(services2) > len(services1):
            services2.reverse()
            services1.append(services2.pop())
            services2.reverse()
    else:
        services1= services
        services2 = []
    context={
        'patrimony':patrimony,
        'material_patrimony':materialPatrimony,
        'activities1':activities1,
        'activities2':activities2,
        'tickets':tickets,
        'services1':services1,
        'services2': services2
    }
    return render(request, 'map/mapaFicha.html',context)