import requests

from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.cache import cache

from ..models import Post
from notifications.forms import PostcodeNotificationForm


class ElectionNotificationFormMixin(object):
    notification_form = PostcodeNotificationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.method == 'POST':
            context['notification_form'] = self.notification_form(
                self.request.POST)
        else:
            context['notification_form'] = self.notification_form()
        return context

    def post(self, request, *args, **kwargs):
        if 'form_name' in request.POST:
            if request.POST['form_name'] == "postcode_notification":
                form = self.notification_form(request.POST)
                if form.is_valid():
                    form.save()
                    request.session['notification_form_filed'] = \
                        form.cleaned_data['postcode']
                    url = request.build_absolute_uri()
                    return HttpResponseRedirect(url)
                else:
                    return self.render_to_response(self.get_context_data())
        return super().post(request, *args, **kwargs)


class PostcodeToPostsMixin(object):
    def postcode_to_posts(self, postcode):
        key = "upcoming_elections_{}".format(postcode)
        results_json = cache.get(key)
        if not results_json:
            url = '{0}/upcoming-elections?postcode={1}'.format(
                settings.YNR_BASE,
                postcode
            )
            req = requests.get(url)
            results_json = req.json()
            cache.set(key, results_json)

        all_posts = []
        for election in results_json:
            all_posts.append(election['post_slug'])

        posts = Post.objects.filter(ynr_id__in=all_posts)
        posts = posts.select_related('election')
        posts = posts.select_related('election__voting_system')
        posts = posts.order_by('election__uses_lists')
        return posts


class PollingStationInfoMixin(object):
    def get_polling_station_info(self, postcode):
        key = "pollingstations_{}".format(postcode)
        info = cache.get(key)
        if info:
            return info

        info = {}
        base_url = "http://pollingstations.democracyclub.org.uk"
        url = "{base_url}/api/postcode/{postcode}/".format(
            base_url=base_url,
            postcode=postcode
        )
        try:
            req = requests.get(url)
        except:
            return info
        if req.status_code != 200:
            return info
        info.update(req.json())
        cache.set(key, info)
        return info
