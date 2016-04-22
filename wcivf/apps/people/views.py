from django.views.generic import DetailView
from django.http import Http404

from .models import Person, PersonPost


class PersonView(DetailView):
    model = Person

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        pk = self.kwargs.get(self.pk_url_kwarg)
        queryset = queryset.filter(ynr_id=pk)
        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404("No %(verbose_name)s found matching the query" %
                          {'verbose_name': queryset.model._meta.verbose_name})

        obj.current_posts = PersonPost.objects.filter(person=obj, post__election__current=True)
        obj.past_posts = PersonPost.objects.filter(person=obj, post__election__current=False)
        return obj
