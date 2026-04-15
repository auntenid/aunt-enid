from django.contrib import admin
from django.utils.html import format_html
from .models import (
    NewsArticle, ManifestoItem, ContactMessage, 
    SiteConfiguration, CoreValue, KabaleFeature
)


@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'location', 'is_published', 'is_featured', 'published_date']
    list_filter = ['category', 'is_published', 'is_featured', 'published_date']
    search_fields = ['title', 'excerpt', 'content']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_date'
    ordering = ['-published_date']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'excerpt', 'content')
        }),
        ('Categorization', {
            'fields': ('category', 'location')
        }),
        ('Media', {
            'fields': ('featured_image', 'image_alt_text')
        }),
        ('Publishing', {
            'fields': ('is_published', 'is_featured', 'published_date')
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related()


@admin.register(ManifestoItem)
class ManifestoItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'icon', 'order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['title', 'description']
    ordering = ['order', 'title']
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'icon', 'description', 'points')
        }),
        ('Display', {
            'fields': ('order', 'is_active')
        }),
    )


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'email', 'message']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Message', {
            'fields': ('message',)
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Site Information', {
            'fields': ('site_name', 'tagline', 'subtitle', 'hero_description')
        }),
        ('Contact Information', {
            'fields': ('phone', 'email', 'location', 'whatsapp')
        }),
        ('Social Media', {
            'fields': ('facebook_url', 'twitter_url', 'instagram_url', 'tiktok_url')
        }),
        ('About Section', {
            'fields': ('about_title', 'about_subtitle', 'why_running', 'vision')
        }),
        ('Kabale Section', {
            'fields': ('kabale_title', 'kabale_subtitle', 'kabale_description')
        }),
        ('Footer', {
            'fields': ('footer_description', 'copyright_text')
        }),
    )
    
    def has_add_permission(self, request):
        # Only allow one configuration instance
        return not SiteConfiguration.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Don't allow deletion of configuration
        return False


@admin.register(CoreValue)
class CoreValueAdmin(admin.ModelAdmin):
    list_display = ['title', 'icon', 'order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['title', 'description']
    ordering = ['order', 'title']
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'icon', 'description')
        }),
        ('Display', {
            'fields': ('order', 'is_active')
        }),
    )


@admin.register(KabaleFeature)
class KabaleFeatureAdmin(admin.ModelAdmin):
    list_display = ['title', 'icon', 'order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['title', 'description']
    ordering = ['order', 'title']
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'icon', 'description')
        }),
        ('Display', {
            'fields': ('order', 'is_active')
        }),
    )


# Customize admin site
admin.site.site_header = "Aunt Enid Campaign Admin"
admin.site.site_title = "Aunt Enid Admin"
admin.site.index_title = "Welcome to Aunt Enid Campaign Administration"