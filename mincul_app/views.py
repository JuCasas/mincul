from django.shortcuts import render


# Create your views here.
def login(request):
    return render(request, 'template_auth.html')


def template(request):
    return render(request, 'template.html')

def material(request):
    return render(request, 'materialKit.html')