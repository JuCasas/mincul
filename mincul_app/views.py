from django.shortcuts import render

# Create your views here.
def template(request):
    return render(request, 'template_auth.html')

def login(request):
    return render(request, 'patrimonio/patrimony_list.html')

def material(request):
    return render(request, 'materialKit.html')
