from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse  # noqa
from django.urls import reverse
# from django.views import generic
from .models import TriggerResponse, get_network
from .forms import TriggerResponseForm, TriggerResponseFormFK
# from . import load


def index(request):
    objForm = TriggerResponseFormFK()
    return render(request, 'chatapp/index.html', {'obj_form': objForm})


def create(request):
    trigForm = TriggerResponseForm()
    return render(request, 'chatapp/create.html', {'trig_form': trigForm})


def save_new_sequence(request, form=TriggerResponseForm, model=TriggerResponse):
    # selected_source = request.POST.get("Source")
    # selected_dest = request.POST.get("Dest")
    # selected_trig = request.POST.get("Trigger")
    # selected_resp = request.POST.get("Response")

    # if selected_resp == "" or selected_trig == "" or selected_source == "" or selected_dest == "":
    #     return render(request, 'chatapp/create.html', {
    #         'error_message': "Please fill all text boxes",
    #     })
    # else:
    #     new_trig = TriggerResponse(dest_state=selected_dest, source_state=selected_source,
    #                                trigger=selected_trig, response=selected_resp)
    #     new_trig.save()
    #     return HttpResponseRedirect(reverse('chatapp:index'))

    form = form(request.POST)
    if form.is_valid():
        obj = model(**form.cleaned_data)
        obj.save()

    return HttpResponseRedirect(reverse('chatapp:index'))


def network_rest(request):
    # call serialize network function
    js = get_network()
    return JsonResponse(js, content_type='application/json', safe=False)  # noqa
