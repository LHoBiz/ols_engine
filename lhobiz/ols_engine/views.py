from tempfile import TemporaryFile
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.
from django.http import HttpResponse
from django.urls import reverse
from django.views import generic
from .models import Aerodrome, Runway

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy

class Register(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('register-success')

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.success_url)
        

class IndexView(generic.ListView):
    template_name = 'ols_engine/index.html'
    context_object_name = 'aerodrome_list'

    def get_queryset(self):
        """Return the list of aerodromes."""
        return Aerodrome.objects.order_by('-name')

class DetailView(generic.DetailView):
    model = Aerodrome
    template_name = 'ols_engine/detail.html'

def runways(request, aerodrome_id):
    response = "You're looking at the runways of aerodrome %s."
    return HttpResponse(response % aerodrome_id)

def generate(request, aerodrome_id):
    aerodrome = get_object_or_404(Aerodrome, pk=aerodrome_id)
    try:
        selected_runway = aerodrome.runway_set.get(pk=request.POST['runway'])
    except (KeyError, Runway.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'ols_engine/detail.html', {
            'aerodrome': aerodrome,
            'error_message': "You didn't select a runway.",
        })
    else:
        selected_runway.generate_ols()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('ols_engine:results', args=(aerodrome.id,)))

class ResultsView(generic.DetailView):
    model = Aerodrome
    template_name = 'ols_engine/results.html'