import requests

from django.views.generic import FormView
from django.conf import settings
from django.core.urlresolvers import reverse

from .forms import PostcodeLookupForm


class PostcodeFormView(FormView):
    form_class = PostcodeLookupForm

    def form_valid(self, form):
        postcode = form.cleaned_data['postcode']
        self.success_url = reverse(
            'postcode_view',
            kwargs={'postcode': postcode}
        )
        return super().form_valid(form)


class HomePageView(PostcodeFormView):
    template_name = "home.html"
