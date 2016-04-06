from django.conf.urls import url
from django.views.generic import TemplateView

from .views import HomePageView

urlpatterns = [
    url(r'^$', HomePageView.as_view(), name="home_view"),
    url(r'^privacy/$',
        TemplateView.as_view(template_name="privacy.html"),
        name="privacy"),
]
