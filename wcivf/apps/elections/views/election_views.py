from django.views.generic import TemplateView, DetailView
from django.http import Http404

from ..models import Election, Post


class ElectionsView(TemplateView):
    template_name = "elections/elections_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_elections = Election.objects.all().order_by(
            '-election_date', 'election_type')

        context['past_elections'] = \
            all_elections.filter(current=False)

        context['current_elections'] = \
            all_elections.filter(current=True)

        return context


class ElectionView(DetailView):
    template_name = "elections/election_view.html"
    model = Election

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        pk = self.kwargs.get(self.pk_url_kwarg)
        queryset = queryset.filter(slug=pk)
        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404("No %(verbose_name)s found matching the query" %
                          {'verbose_name': queryset.model._meta.verbose_name})
        return obj


class PostView(DetailView):
    template_name = "elections/post_view.html"
    model = Post

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        pk = self.kwargs.get('post_id')
        queryset = queryset.filter(ynr_id=pk)
        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404("No %(verbose_name)s found matching the query" %
                          {'verbose_name': queryset.model._meta.verbose_name})
        return obj
