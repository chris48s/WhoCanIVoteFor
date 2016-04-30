from django.conf.urls import url
from django.views.generic import TemplateView

from .views import HomePageView, PostcodeFormView

urlpatterns = [
    url(r'^$', HomePageView.as_view(), name="home_view"),
    url(r'^privacy/$',
        TemplateView.as_view(template_name="privacy.html"),
        name="privacy_view"),
    url(r'^about/$',
        TemplateView.as_view(template_name="about.html"),
        name="about_view"),

    url(r'^london-mayoral-election-2016',
        PostcodeFormView.as_view(template_name='seo-landing-pages/london_mayoral_2016.html'),
        name='seo-mayoral-2016'
    ),
    url(r'^london-elections-2016',
        PostcodeFormView.as_view(template_name='seo-landing-pages/london_elections_2016.html'),
        name='seo-london-2016'),
    url(r'^london-assembly-2016',
        PostcodeFormView.as_view(template_name='seo-landing-pages/london_assembly_2016.html'),
        name='seo-london-assembly-2016'),

    url(r'^scotland-2016',
        PostcodeFormView.as_view(template_name='seo-landing-pages/scottish_parliament_2016.html'),
        name='seo-scotland-2016'),
    url(r'^scottish-parliament-2016',
        PostcodeFormView.as_view(template_name='seo-landing-pages/scottish_parliament_2016.html'),
        name='seo-scottish-parliament-2016'),
    url(r'^holyrood-2016',
        PostcodeFormView.as_view(template_name='seo-landing-pages/scottish_parliament_2016.html'),
        name='seo-holyrood-2016'),

    url(r'^local-elections-2016',
        PostcodeFormView.as_view(template_name='seo-landing-pages/local_elections_2016.html'),
        name='seo-local-2016'),

    url(r'^wales-2016',
        PostcodeFormView.as_view(template_name='seo-landing-pages/welsh_2016.html'),
        name='seo-wales-2016'),
    url(r'^welsh-assembly-2016',
        PostcodeFormView.as_view(template_name='seo-landing-pages/welsh_2016.html'),
        name='seo-welsh-assembly-2016'),
    url(r'^senedd-2016',
        PostcodeFormView.as_view(template_name='seo-landing-pages/welsh_2016.html'),
        name='seo-senedd-2016'),

    url(r'^police-and-crime-commissioner-elections-2016',
        PostcodeFormView.as_view(template_name='seo-landing-pages/pcc_2016.html'),
        name='seo-pcc-2016'),

    url(r'^northern-ireland-assembly-2016',
        PostcodeFormView.as_view(template_name='seo-landing-pages/ni_ass_2016.html'),
        name='seo-ni-2016'),

    url(r'^bristol-mayoral-2016',
        PostcodeFormView.as_view(template_name='seo-landing-pages/bristol_mayor_2016.html'),
        name='seo-bristol-2016'),

    url(r'^liverpool-mayoral-2016',
        PostcodeFormView.as_view(template_name='seo-landing-pages/liverpool_mayor_2016.html'),
        name='seo-liverpool-2016'),

    url(r'^salford-mayoral-2016',
        PostcodeFormView.as_view(template_name='seo-landing-pages/salford_mayor_2016.html'),
        name='seo-salford-2016'),

    url(r'^seo-fun-times',
        PostcodeFormView.as_view(template_name='seo-landing-pages/index.html'),
        name='seo-index'),

]
