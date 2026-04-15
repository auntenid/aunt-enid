from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from .models import NewsArticle, ManifestoItem, ContactMessage, CoreValue, KabaleFeature
from .forms import ContactForm


def home(request):
    """Homepage view"""
    # Get featured news articles
    featured_articles = NewsArticle.objects.filter(
        is_published=True, 
        is_featured=True
    ).order_by('-published_date')[:6]
    
    # Get all published articles for news section
    all_articles = NewsArticle.objects.filter(is_published=True).order_by('-published_date')[:6]
    
    # Get manifesto items
    manifesto_items = ManifestoItem.objects.filter(is_active=True).order_by('order')
    
    # Get core values
    core_values = CoreValue.objects.filter(is_active=True).order_by('order')
    
    # Get Kabale features
    kabale_features = KabaleFeature.objects.filter(is_active=True).order_by('order')
    
    context = {
        'featured_articles': featured_articles,
        'all_articles': all_articles,
        'manifesto_items': manifesto_items,
        'core_values': core_values,
        'kabale_features': kabale_features,
    }
    
    return render(request, 'website/home.html', context)


def article_detail(request, slug):
    """Individual article detail view"""
    article = get_object_or_404(NewsArticle, slug=slug, is_published=True)
    
    context = {
        'article': article,
    }
    
    return render(request, 'website/article_detail.html', context)


def news_list(request):
    """News listing page"""
    articles = NewsArticle.objects.filter(is_published=True).order_by('-published_date')
    
    # Pagination
    paginator = Paginator(articles, 9)  # 9 articles per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'articles': page_obj,
    }
    
    return render(request, 'website/news_list.html', context)


def contact(request):
    """Contact page view"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Save the contact message
            contact_message = form.save()
            messages.success(request, 'Thank you for your message! We will get back to you soon.')
            return redirect('contact')
    else:
        form = ContactForm()
    
    context = {
        'form': form,
    }
    
    return render(request, 'website/contact.html', context)


def about(request):
    """About page view"""
    # Get core values
    core_values = CoreValue.objects.filter(is_active=True).order_by('order')
    
    context = {
        'core_values': core_values,
    }
    
    return render(request, 'website/about.html', context)


def manifesto(request):
    """Manifesto page view"""
    # Get manifesto items
    manifesto_items = ManifestoItem.objects.filter(is_active=True).order_by('order')
    
    context = {
        'manifesto_items': manifesto_items,
    }
    
    return render(request, 'website/manifesto.html', context)


def kabale(request):
    """Kabale District page view"""
    # Get Kabale features
    kabale_features = KabaleFeature.objects.filter(is_active=True).order_by('order')
    
    context = {
        'kabale_features': kabale_features,
    }
    
    return render(request, 'website/kabale.html', context)


@csrf_exempt
@require_http_methods(["POST"])
def contact_ajax(request):
    """AJAX contact form submission"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = form.save()
            return JsonResponse({
                'success': True,
                'message': 'Thank you for your message! We will get back to you soon.'
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            })
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})


def sitemap(request):
    """Generate sitemap for SEO"""
    articles = NewsArticle.objects.filter(is_published=True).order_by('-published_date')
    
    context = {
        'articles': articles,
    }
    
    return render(request, 'website/sitemap.xml', context, content_type='application/xml')


def robots_txt(request):
    """Generate robots.txt for SEO"""
    return render(request, 'website/robots.txt', content_type='text/plain')