"""
URL configuration for aunt_enid_campaign project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import os
import hashlib
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.http import FileResponse, Http404


def cached_media_serve(request, path):
    """
    Serve media files with aggressive caching headers so that:
      - Browsers cache images for 1 year (no re-download on revisit)
      - WhatsApp / Facebook scrapers download images quickly (they honour Cache-Control)
      - ETags prevent unnecessary re-downloads even after the 1-year window

    This replaces Django's bare serve() which sends no cache headers at all.
    """
    full_path = os.path.join(settings.MEDIA_ROOT, path)
    if not os.path.exists(full_path) or not os.path.isfile(full_path):
        raise Http404("Media file not found")

    # Build a strong ETag from the file's size + mtime (cheap, no hash needed)
    stat = os.stat(full_path)
    etag = f'"{stat.st_size}-{int(stat.st_mtime)}"'

    # Honour If-None-Match for 304 Not Modified
    if request.META.get('HTTP_IF_NONE_MATCH') == etag:
        from django.http import HttpResponse
        response = HttpResponse(status=304)
        response['ETag'] = etag
        return response

    response = FileResponse(open(full_path, 'rb'))
    response['Cache-Control'] = 'public, max-age=31536000, immutable'
    response['ETag'] = etag
    return response


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('website.urls')),
    # Serve media files with caching headers (scrapers + browsers cache aggressively)
    re_path(r'^media/(?P<path>.*)$', cached_media_serve),
]

# Serve static files only in DEBUG (WhiteNoise handles them in production)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)