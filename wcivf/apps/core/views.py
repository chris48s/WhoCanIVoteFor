import requests

from django.views.generic import FormView
from django.conf import settings
from django.core.urlresolvers import reverse

from .forms import PostcodeLookupForm


class HomePageView(FormView):
    template_name = "home.html"
    form_class = PostcodeLookupForm

    def form_valid(self, form):
        postcode = form.cleaned_data['postcode']
        self.success_url = reverse(
            'postcode_view',
            kwargs={'postcode': postcode}
        )
        return super().form_valid(form)

