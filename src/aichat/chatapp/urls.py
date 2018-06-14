from django.urls import path
from .models import node_autocomplete
from . import views

app_name = 'chatapp'
urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('create/save/', views.save_new_sequence, name='save'),
    path('network.json', views.network_rest, name='network'),
    path('node_autocomplete', node_autocomplete.as_view(), name='node_autocomplete')
]
