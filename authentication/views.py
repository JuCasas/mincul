from django.shortcuts import render

# Create your views here.

import requests
from django.views.generic import CreateView


class RenderLogin(CreateView):
    # template_name = 'authentication/login.html'

    def get_context_data(self, **kwargs):
        context = {

        }
        return context
