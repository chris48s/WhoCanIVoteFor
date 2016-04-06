from django.conf import settings

def canonical_url(request):
    return {'CANONICAL_URL': settings.CANONICAL_URL}
