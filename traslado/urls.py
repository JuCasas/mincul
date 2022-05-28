from django.urls import path
from traslado import views

urlpatterns = [

    path('add/',views.addTransfer, name='addProject'),

]