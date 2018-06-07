from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse # noqa
from django.urls import reverse
# from django.views import generic
from .models import TriggerResponse, get_network
# from . import load


def index(request):
    return render(request, 'chatapp/index.html', )


def create(request):
    return render(request, 'chatapp/create.html')


def save_new_sequence(request):
    selected_source = request.POST.get("Source")
    selected_dest = request.POST.get("Dest")
    selected_trig = request.POST.get("Trigger")
    selected_resp = request.POST.get("Response")
    if selected_resp == "" or selected_trig == "" or selected_source == "" or selected_dest == "":
        return render(request, 'chatapp/create.html', {
            'error_message': "Please fill all text boxes",
        })
    else:
        new_trig = TriggerResponse(dest_state=selected_dest, source_state=selected_source,
                                   trigger=selected_trig, response=selected_resp)
        new_trig.save()
        return HttpResponseRedirect(reverse('chatapp:index'))


def network_rest(request):
    # call serialize network function
    js = get_network()
    return JsonResponse(js, content_type='application/json', safe=False)  # noqa
