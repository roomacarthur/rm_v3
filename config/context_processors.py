from django.conf import settings


# context processor to get correct site url for SEO.
def site_url(request):
    return {
        'SITE_URL': settings.SITE_URL
    }
