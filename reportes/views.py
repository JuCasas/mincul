from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect

# Create your views here.
def reportes(request):
    return render(request, 'reportes/reportes_gestor.html')


def traerData(request):
    # data = Client_Category.objects.get(client_id=request.POST['pk'], state=True, type=request.POST['type'])
    # categoryS = serializers.serialize("json", [category.category, ])
    data = {'traerData': [10, 20, 20, 20, 20, 25]}
    return JsonResponse({"data": data}, status=200)


def traerNombres(request):
    return render(request, 'reportes/reportes_gestor.html')
