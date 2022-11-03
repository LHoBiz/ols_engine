from tempfile import TemporaryFile
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.http import Http404
# Create your views here.
from django.http import HttpResponse

from .models import Aerodrome

def index(request):
    aerodrome_list = Aerodrome.objects.order_by('-name')
    template = loader.get_template('ols_engine/index.html')
    context = {
        'aerodrome_list': aerodrome_list,
    }
    return HttpResponse(template.render(context, request))

def detail(request, aerodrome_id):
    aerodrome = get_object_or_404(Aerodrome, pk=aerodrome_id) 
    return render(request, 'ols_engine/detail.html', {'aerodrome': aerodrome})

def runways(request, aerodrome_name):
    response = "You're looking at the runways of aerodrome %s."
    return HttpResponse(response % aerodrome_name)

def generate(request, aerodrome_name):
    return HttpResponse("You're generating ols for aerodrome %s." % aerodrome_name)
