from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
# from django.views import generic
from .models import TriggerResponse


def index(request):
    return render(request, 'chatapp/index.html', )


def create(request):
    return render(request, 'chatapp/create.html')


def save_new_sequence(request):
    try:
        selected_source = TriggerResponse.get(pk=request.POST['Source'])
        selected_dest = TriggerResponse.get(pk=request.POST['Dest'])
        selected_trig = TriggerResponse.get(pk=request.POST['Trigger'])
        selected_resp = TriggerResponse.get(pk=request.POST['Response'])

    except KeyError:
        # Redisplay the textboxes
        return render(request, 'create', {
            'error_message': "Please fill all text boxes",
        })
    else:
        new_trig = TriggerResponse(dest_state=selected_dest, source_state=selected_source,
                                   trigger=selected_trig, response=selected_resp)
        new_trig.save()
        return HttpResponseRedirect(reverse('states:index'))
