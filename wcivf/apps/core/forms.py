from django import forms

from localflavor.gb.forms import GBPostcodeField


class PostcodeLookupForm(forms.Form):
    postcode = GBPostcodeField(label="Enter your postcode")

    def __init__(self, *args, **kwargs):
        super(PostcodeLookupForm, self).__init__(*args, **kwargs)
        self.fields['postcode'].widget.attrs['autofocus'] = u'autofocus'
