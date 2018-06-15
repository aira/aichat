from django.urls import path
from .models import node_obj_autocomplete, node_autocomplete, Node  # noqa
from . import views
from dal import autocomplete

app_name = 'chatapp'
urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('create/save/', views.save_new_sequence, name='save'),
    path('network.json', views.network_rest, name='network'),
    path('node_autocomplete', node_autocomplete.as_view(), name='node_autocomplete'),
    path('node_obj_autocomplete', autocomplete.Select2QuerySetView.as_view(model=Node), name='node_obj_autocomplete')
]
