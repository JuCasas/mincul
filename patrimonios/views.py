from django.shortcuts import render

# Create your views here.
def patrimony_list(request):
    return render(request, 'patrimony/patrimony_list.html')