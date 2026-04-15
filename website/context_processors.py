from .models import SiteConfiguration


def site_config(request):
    """Context processor to make site configuration available in all templates"""
    try:
        config = SiteConfiguration.objects.first()
        if not config:
            # Create default configuration if none exists
            config = SiteConfiguration.objects.create()
    except SiteConfiguration.DoesNotExist:
        config = SiteConfiguration.objects.create()
    
    return {
        'site_config': config,
    }
