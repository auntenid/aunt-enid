from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify


class NewsArticle(models.Model):
    """Model for news articles"""
    CATEGORY_CHOICES = [
        ('leadership', 'Leadership'),
        ('politics', 'Politics'),
        ('campaign', 'Campaign'),
        ('empowerment', 'Empowerment'),
        ('youth', 'Youth'),
        ('clarification', 'Clarification'),
        ('nrm_event', 'NRM Event'),
        ('women_empowerment', 'Women Empowerment'),
        ('youth_development', 'Youth Development'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    excerpt = models.TextField(max_length=500, help_text="Short description for news preview")
    content = models.TextField(help_text="Full article content")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    location = models.CharField(max_length=100, default="Kabale District")
    featured_image = models.ImageField(upload_to='news_images/', blank=True, null=True)
    image_alt_text = models.CharField(max_length=200, blank=True)
    published_date = models.DateTimeField(default=timezone.now)
    is_published = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False, help_text="Show on homepage")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-published_date']
        verbose_name = "News Article"
        verbose_name_plural = "News Articles"
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('website:article_detail', kwargs={'slug': self.slug})


class ManifestoItem(models.Model):
    """Model for manifesto items"""
    ICON_CHOICES = [
        ('graduation-cap', 'Education & Youth'),
        ('female', 'Women Empowerment'),
        ('leaf', 'Agriculture'),
        ('road', 'Infrastructure'),
        ('chart-line', 'Economic Development'),
        ('shield-alt', 'Community Security'),
    ]
    
    title = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, choices=ICON_CHOICES)
    description = models.TextField()
    points = models.JSONField(default=list, help_text="List of bullet points")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'title']
        verbose_name = "Manifesto Item"
        verbose_name_plural = "Manifesto Items"
    
    def __str__(self):
        return self.title


class ContactMessage(models.Model):
    """Model for contact form submissions"""
    STATUS_CHOICES = [
        ('new', 'New'),
        ('read', 'Read'),
        ('replied', 'Replied'),
        ('closed', 'Closed'),
    ]
    
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"
    
    def __str__(self):
        return f"{self.name} - {self.created_at.strftime('%Y-%m-%d')}"


class SiteConfiguration(models.Model):
    """Model for site-wide configuration"""
    site_name = models.CharField(max_length=100, default="Aunt Enid Campaign")
    tagline = models.CharField(max_length=200, default="Aspiring Woman Member of Parliament")
    subtitle = models.CharField(max_length=200, default="NRM FLAG BEARER Kabale District 2026-2031")
    hero_description = models.TextField(default="A compassionate leader who empowers, connects, and transforms communities")
    
    # Contact Information
    phone = models.CharField(max_length=20, default="0764195740")
    email = models.EmailField(default="auntenidoa@gmail.com")
    location = models.CharField(max_length=100, default="Kabale District, Uganda")
    whatsapp = models.CharField(max_length=20, default="+256 705 357149")
    
    # Social Media Links
    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    tiktok_url = models.URLField(default="https://tiktok.com/@auntenid")
    
    # About Section
    about_title = models.CharField(max_length=100, default="Who is Aunt Enid?")
    about_subtitle = models.CharField(max_length=200, default="A dedicated community leader with a heart for service and transformation")
    why_running = models.TextField(default="As a woman leader deeply rooted in Kabale District, I believe in the power of inclusive governance...")
    vision = models.TextField(default="I envision a Kabale District where every family thrives...")
    
    # Kabale Section
    kabale_title = models.CharField(max_length=100, default="Kabale District")
    kabale_subtitle = models.CharField(max_length=200, default="Our beautiful home with unlimited potential")
    kabale_description = models.TextField(default="Kabale, often called the 'Switzerland of Africa'...")
    
    # Footer
    footer_description = models.TextField(default="Empowering Kabale District through compassionate leadership and inclusive development.")
    copyright_text = models.CharField(max_length=200, default="2025 Aunt Enid Campaign. All rights reserved.")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Site Configuration"
        verbose_name_plural = "Site Configuration"
    
    def __str__(self):
        return "Site Configuration"
    
    def save(self, *args, **kwargs):
        # Ensure only one configuration instance exists
        if not self.pk and SiteConfiguration.objects.exists():
            return
        super().save(*args, **kwargs)


class CoreValue(models.Model):
    """Model for core values section"""
    title = models.CharField(max_length=50)
    icon = models.CharField(max_length=50, help_text="FontAwesome icon class")
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'title']
        verbose_name = "Core Value"
        verbose_name_plural = "Core Values"
    
    def __str__(self):
        return self.title


class KabaleFeature(models.Model):
    """Model for Kabale District features"""
    title = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, help_text="FontAwesome icon class")
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'title']
        verbose_name = "Kabale Feature"
        verbose_name_plural = "Kabale Features"
    
    def __str__(self):
        return self.title