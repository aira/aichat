from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse  # noqa
from django.urls import reverse
from .models import TriggerResponse, get_network
from .forms import TriggerResponseForm
# from . import load


def index(request):
    trigForm = TriggerResponseForm()
    return render(request, 'chatapp/index.html', {'trig_form': trigForm})


def create(request):
    trigForm = TriggerResponseForm()
    return render(request, 'chatapp/create.html', {'trig_form': trigForm})


def save_new_sequence(request, form=TriggerResponseForm, model=TriggerResponse):
    form = form(request.POST)
    if form.is_valid():
        obj = model(**form.cleaned_data)
        obj.save()
    return HttpResponseRedirect(reverse('chatapp:index'))


def network_rest(request):
    # call serialize network function
    js = get_network()
    return JsonResponse(js, content_type='application/json', safe=False)  # noqa
