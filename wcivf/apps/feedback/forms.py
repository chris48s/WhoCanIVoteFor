from django import forms

from .models import Feedback, FOUND_USEFUL_CHOICES


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['found_useful', 'comments', 'source_url']

    found_useful = forms.ChoiceField(
        choices=FOUND_USEFUL_CHOICES,
        widget=forms.RadioSelect(
            attrs={
                'data-toggle': "button",
            }
        )
    )
    source_url = forms.CharField(widget=forms.HiddenInput())
