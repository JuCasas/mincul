from django.shortcuts import render


# Create your views here.
def template(request):
    return render(request, 'template_auth.html')

def detalle(request):
    return render(request, 'templateDetail.html')

def login(request):
    return render(request, 'template.html')

def material(request):
    return render(request, 'materialKit.html')