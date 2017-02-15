import datetime

import requests

from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.cache import cache

from notifications.forms import PostcodeNotificationForm
from core.models import LoggedPostcode
from ..models import Post, Election, InvalidPostcodeError


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

    def save_postcode_to_session(self, postcode):
        notification_for_postcode = self.request.session.get(
            'notification_for_postcode', [])
        notification_for_postcode.append(postcode)
        self.request.session['notification_for_postcode'] = \
            notification_for_postcode
        self.request.session.modified = True

    def post(self, request, *args, **kwargs):
        if 'form_name' in request.POST:
            if request.POST['form_name'] == "postcode_notification":
                form = self.notification_form(request.POST)
                if form.is_valid():
                    form.save()
                    self.save_postcode_to_session(
                        form.cleaned_data['postcode'])
                    url = request.build_absolute_uri()
                    return HttpResponseRedirect(url)
                else:
                    return self.render_to_response(self.get_context_data())
        return super().post(request, *args, **kwargs)


class PostcodeToPostsMixin(object):
    def get(self, request, *args, **kwargs):
        try:
            context = self.get_context_data(**kwargs)
        except InvalidPostcodeError:
            return HttpResponseRedirect(
                '/?invalid_postcode=1&postcode={}'.format(
                    self.postcode
                ))
        return self.render_to_response(context)

    @property
    def should_add_eu(self):
        return datetime.datetime.now().timestamp() < 1466719200

    def add_eu(self):
        election, _ = Election.objects.update_or_create(
            slug="ref.2016-06-23",
            election_date="2016-06-23",
            name="Referendum on the UK's membership of the European Union",
            current=True,
            defaults={
                'election_type': "ref",
            }
        )
        if not self.should_add_eu:
            # Don't do anyting if the election is in the past
            if election.current:
                election.current = False
                election.save()
            return
        eu_post, _ = Post.objects.update_or_create(
            ynr_id="ref.2016-06-23",
            label="EU Referendum",
            role="Referendum on the UK's membership of the European Union",
            group="UK",
            organization="UK Government",
            area_name="UK",
            area_id="GB",
            election=election
        )
        return eu_post.ynr_id

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

        if type(results_json) == dict and 'error' in results_json.keys():
            raise InvalidPostcodeError(postcode)
        all_posts = []
        for election in results_json:
            all_posts.append(election['post_slug'])
        if self.should_add_eu:
            all_posts.append(self.add_eu())
        print(all_posts)



        posts = Post.objects.filter(ynr_id__in=all_posts)
        posts = posts.select_related('election')
        posts = posts.select_related('election__voting_system')
        posts = posts.order_by(
            'election__election_date',
            'election__election_weight'
        )
        return posts


class PollingStationInfoMixin(object):
    def get_polling_station_info(self, postcode):
        key = "pollingstations_{}".format(postcode)
        info = cache.get(key)
        if info:
            return info

        info = {}
        base_url = settings.WDIV_BASE + settings.WDIV_API
        url = "{base_url}/postcode/{postcode}.json".format(
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


class LogLookUpMixin(object):
    def log_postcode(self, postcode):
        kwargs = {
            'postcode': postcode,
        }
        kwargs.update(self.request.session['utm_data'])
        LoggedPostcode.objects.create(**kwargs)
