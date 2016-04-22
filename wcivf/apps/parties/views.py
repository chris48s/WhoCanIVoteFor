from django.views.generic import ListView, DetailView

from .models import Party

class PartiesView(ListView):
    queryset = Party.objects.exclude(personpost=None)

class PartyView(DetailView):
    queryset = Party.objects.all()
