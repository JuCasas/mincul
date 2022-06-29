from django.shortcuts import render


def error_404_view(request, exception):
    template_name = 'errors/error404.html'
    return render(request, template_name=template_name)

def error_500_view(request):
    template_name = 'errors/error500.html'
    return render(request, template_name=template_name)