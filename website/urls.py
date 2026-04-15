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
    
    # SEO
    path('sitemap.xml', views.sitemap, name='sitemap'),
    path('robots.txt', views.robots_txt, name='robots_txt'),
]
