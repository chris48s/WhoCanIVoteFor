from django.conf.urls import url

from .views import FeedbackFormView

urlpatterns = [
    url(
        r'^$',
        FeedbackFormView.as_view(),
        name='feedback_form_view'),
]
