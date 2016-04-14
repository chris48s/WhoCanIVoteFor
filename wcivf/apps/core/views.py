import requests

from django.views.generic import FormView
from django.conf import settings
from django.core.urlresolvers import reverse

from .forms import PostcodeLookupForm
from .models import LoggedPostcode

class LogLookUpMixin(object):
    def log_postcode(self, postcode):
        kwargs = {
            'postcode': postcode,
        }
        kwargs.update(self.request.session['utm_data'])
        LoggedPostcode.objects.create(**kwargs)


class HomePageView(LogLookUpMixin, FormView):
    template_name = "home.html"
    form_class = PostcodeLookupForm

    def form_valid(self, form):
        postcode = form.cleaned_data['postcode']
        self.log_postcode(postcode)
        self.success_url = reverse(
            'postcode_view',
            kwargs={'postcode': postcode}
        )
        return super().form_valid(form)

