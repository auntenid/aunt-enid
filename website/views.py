from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from .models import (
    NewsArticle, ManifestoItem, ContactMessage, CoreValue, KabaleFeature,
    ProjectCategory, ImpactProject, GalleryCategory, GalleryItem,
)
from .forms import ContactForm


def home(request):
    """Homepage view"""
    featured_articles = NewsArticle.objects.filter(
        is_published=True,
        is_featured=True
    ).order_by('-published_date')[:6]

    all_articles = NewsArticle.objects.filter(is_published=True).order_by('-published_date')[:6]
    manifesto_items = ManifestoItem.objects.filter(is_active=True).order_by('order')
    core_values = CoreValue.objects.filter(is_active=True).order_by('order')
    kabale_features = KabaleFeature.objects.filter(is_active=True).order_by('order')

    # Featured impact projects for the homepage
    featured_projects = ImpactProject.objects.filter(is_featured=True, is_active=True).order_by('order')[:3]

    context = {
        'featured_articles': featured_articles,
        'all_articles': all_articles,
        'manifesto_items': manifesto_items,
        'core_values': core_values,
        'kabale_features': kabale_features,
        'featured_projects': featured_projects,
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

    paginator = Paginator(articles, 9)
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
            form.save()
            messages.success(request, 'Thank you for your message! We will get back to you soon.')
            return redirect('website:contact')
    else:
        form = ContactForm()

    context = {
        'form': form,
    }

    return render(request, 'website/contact.html', context)


def about(request):
    """About page view"""
    core_values = CoreValue.objects.filter(is_active=True).order_by('order')
    context = {
        'core_values': core_values,
    }
    return render(request, 'website/about.html', context)


def manifesto(request):
    """Redirect to NRM Manifesto PDF"""
    from django.http import HttpResponseRedirect
    return HttpResponseRedirect('https://www.nrm.ug/sites/default/files/2025-09/NRM%20Manifesto%202026-2031.pdf')


def kabale(request):
    """Kabale District page"""
    kabale_features = KabaleFeature.objects.filter(is_active=True).order_by('order')
    context = {
        'kabale_features': kabale_features,
    }
    return render(request, 'website/kabale.html', context)


def sitemap(request):
    """Sitemap XML view"""
    return render(request, 'website/sitemap.xml', content_type='application/xml')


def robots_txt(request):
    """Robots.txt view"""
    lines = [
        "User-agent: *",
        "Allow: /",
        f"Sitemap: {request.scheme}://{request.get_host()}/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


@csrf_exempt
@require_http_methods(["POST"])
def contact_ajax(request):
    """AJAX contact form"""
    try:
        import json
        data = json.loads(request.body)
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        phone = data.get('phone', '').strip()
        message = data.get('message', '').strip()

        if not all([name, email, message]):
            return JsonResponse({'success': False, 'error': 'Please fill in all required fields.'})

        ContactMessage.objects.create(
            name=name,
            email=email,
            phone=phone,
            message=message
        )

        return JsonResponse({'success': True, 'message': 'Thank you for your message!'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


# ==================== IMPACT VIEWS ====================

def impact_list(request):
    """List all impact projects, with optional category filtering"""
    categories = ProjectCategory.objects.all()
    category_slug = request.GET.get('category')
    active_category = None

    projects = ImpactProject.objects.filter(is_active=True)

    if category_slug:
        active_category = get_object_or_404(ProjectCategory, slug=category_slug)
        projects = projects.filter(category=active_category)

    paginator = Paginator(projects, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'categories': categories,
        'projects': page_obj,
        'active_category': active_category,
    }

    return render(request, 'website/impact_list.html', context)


def impact_category(request, slug):
    """Filter impact projects by category"""
    return redirect(f'/impact/?category={slug}')


def impact_detail(request, slug):
    """Detail view for a single impact project"""
    project = get_object_or_404(ImpactProject, slug=slug, is_active=True)
    related_projects = ImpactProject.objects.filter(
        is_active=True, category=project.category
    ).exclude(pk=project.pk)[:3]

    context = {
        'project': project,
        'related_projects': related_projects,
    }

    return render(request, 'website/impact_detail.html', context)


# ==================== GALLERY VIEWS ====================

def gallery_list(request):
    """Gallery listing with optional category and media_type filtering"""
    categories = GalleryCategory.objects.all()
    category_slug = request.GET.get('category')
    media_type = request.GET.get('type')
    active_category = None

    items = GalleryItem.objects.filter(is_active=True)

    if category_slug:
        active_category = get_object_or_404(GalleryCategory, slug=category_slug)
        items = items.filter(category=active_category)

    if media_type in ('image', 'video'):
        items = items.filter(media_type=media_type)

    paginator = Paginator(items, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'categories': categories,
        'items': page_obj,
        'active_category': active_category,
        'active_type': media_type,
    }

    return render(request, 'website/gallery_list.html', context)