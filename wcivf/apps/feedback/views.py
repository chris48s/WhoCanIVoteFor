from django.views.generic import CreateView
from django.utils.http import is_safe_url
from django.contrib import messages

from .forms import FeedbackForm


class FeedbackFormView(CreateView):
    form_class = FeedbackForm
    template_name = "feedback/feedback_form_view.html"

    def get_success_url(self):

        messages.success(self.request, 'Thank you for your feedback!')

        if is_safe_url(self.object.source_url):
            return self.object.source_url
        else:
            return "/"
