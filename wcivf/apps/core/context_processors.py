from django.conf import settings

from .forms import PostcodeLookupForm

def canonical_url(request):
    return {'CANONICAL_URL': settings.CANONICAL_URL}

def use_compress_css(request):
    return {
        'USE_COMPRESSED_CSS': getattr(settings, 'USE_COMPRESSED_CSS', False)
    }

def postcode_form(request):
    return {
        'postcode_form': PostcodeLookupForm()
    }
