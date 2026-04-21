from django.db import OperationalError, ProgrammingError
from .models import SiteConfiguration


def site_config(request):
    """Context processor to make site configuration available in all templates"""
    try:
        config = SiteConfiguration.objects.first()
        if not config:
            config = SiteConfiguration.objects.create()
    except (SiteConfiguration.DoesNotExist, OperationalError, ProgrammingError):
        config = None
    
    return {
        'site_config': config,
    }
