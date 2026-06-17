from django.urls import path
from . import views

app_name = 'website'

urlpatterns = [
    # Main pages
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('manifesto/', views.manifesto, name='manifesto'),
    path('news/', views.news_list, name='news_list'),
    path('kabale/', views.kabale, name='kabale'),
    path('contact/', views.contact, name='contact'),

    # Article pages
    path('article/<slug:slug>/', views.article_detail, name='article_detail'),

    # AJAX endpoints
    path('contact-ajax/', views.contact_ajax, name='contact_ajax'),

    # Impact pages
    path('impact/', views.impact_list, name='impact_list'),
    path('impact/category/<slug:slug>/', views.impact_category, name='impact_category'),
    path('impact/<slug:slug>/', views.impact_detail, name='impact_detail'),

    # Gallery pages
    path('gallery/', views.gallery_list, name='gallery_list'),

    # SEO
    path('sitemap.xml', views.sitemap, name='sitemap'),
    path('robots.txt', views.robots_txt, name='robots_txt'),
]
