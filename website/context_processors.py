from django.db import OperationalError, ProgrammingError
from .models import SiteConfiguration, ProjectCategory


def site_config(request):
    """Context processor to make site configuration and nav data available in all templates"""
    try:
        config = SiteConfiguration.objects.first()
        if not config:
            config = SiteConfiguration.objects.create()
    except (SiteConfiguration.DoesNotExist, OperationalError, ProgrammingError):
        config = None

    # Load Impact categories for the dropdown nav
    try:
        impact_categories = list(ProjectCategory.objects.all().order_by('order'))
    except (OperationalError, ProgrammingError):
        impact_categories = []

    return {
        'site_config': config,
        'impact_categories': impact_categories,
    }
