from django.views.defaults import page_not_found

def error_404_view(request, exception):
    template_name = 'error404/error.html'
    return page_not_found(request, template_name=template_name)