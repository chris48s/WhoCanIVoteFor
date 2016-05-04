import requests

from django.views.generic import FormView
from django.conf import settings
from django.core.urlresolvers import reverse

from .forms import PostcodeLookupForm


class PostcodeFormView(FormView):
    form_class = PostcodeLookupForm

    def get_initial(self):
        initial = self.initial.copy()
        if 'invalid_postcode' in self.request.GET:
            initial['postcode'] = self.request.GET.get('postcode')
        return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'autofocus': True})
        return kwargs

    def form_valid(self, form):
        postcode = form.cleaned_data['postcode']
        self.success_url = reverse(
            'postcode_view',
            kwargs={'postcode': postcode}
        )
        return super().form_valid(form)


class HomePageView(PostcodeFormView):
    template_name = "home.html"
