from django.shortcuts import render
from django.http import HttpResponse
from django import forms
#from .forms import ReqForm
from django.views.generic import CreateView
from .models import slotrequest,District,State
from .forms import RequestByPinForm,RequestByDistForm
# Create your views here.

class ReqestByPinView(CreateView):
    model = slotrequest
    form_class = RequestByPinForm
    success_url = "submitted"

class ReqestByDistView(CreateView):
    model = slotrequest
    form_class = RequestByDistForm
    success_url = "submitted"



def load_districts(request):
    state_id = request.GET.get('state')
    districts = District.objects.filter(state_id=state_id)
    return render(request, 'slots/districts_dropdown_list_options.html', {'districts': districts})
#index for testing purpose
def index(request):
    context = {}
    form = ReqForm(request.POST or None)
    if form.is_valid():
        form.save()
    context['form'] = form
    return render(request, "slots/index.html",context)


def submitted(request):
    return render(request, "slots/submitted.html")


def distslots(request):
    context = {}
    form = RequestByDistForm(request.POST or None)
    if form.is_valid():
        form.save()
    context['form'] = form
    return render(request, "slots/slotrequest_form.html",context)


