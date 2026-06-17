from django.contrib import admin
from django.utils.html import format_html
from .models import (
    NewsArticle, ManifestoItem, ContactMessage,
    SiteConfiguration, CoreValue, KabaleFeature,
    ProjectCategory, ImpactProject,
    GalleryCategory, GalleryItem,
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
        ('About Section - Part 1', {
            'fields': ('about_title', 'about_subtitle', 'about_part1_title', 'about_part1_text'),
            'description': 'Edit the content of the first section on the About page.'
        }),
        ('About Section - Part 2', {
            'fields': ('about_part2_title', 'about_part2_text'),
            'description': 'Edit the content of the second section on the About page.'
        }),
        ('Kabale Section', {
            'fields': ('kabale_title', 'kabale_subtitle', 'kabale_description')
        }),
        ('Footer', {
            'fields': ('footer_description', 'copyright_text')
        }),
    )

    def has_add_permission(self, request):
        return not SiteConfiguration.objects.exists()

    def has_delete_permission(self, request, obj=None):
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


# ==================== IMPACT ADMIN ====================

@admin.register(ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon', 'order', 'project_count']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['order', 'name']

    fieldsets = (
        ('Category Details', {
            'fields': ('name', 'slug', 'icon', 'description')
        }),
        ('Display', {
            'fields': ('order',)
        }),
    )

    def project_count(self, obj):
        count = obj.projects.filter(is_active=True).count()
        return format_html('<b>{}</b> projects', count)
    project_count.short_description = "Active Projects"


@admin.register(ImpactProject)
class ImpactProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'location', 'date_completed', 'beneficiaries', 'is_featured', 'is_active']
    list_filter = ['category', 'is_featured', 'is_active', 'date_completed']
    search_fields = ['title', 'excerpt', 'description', 'location']
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['-date_completed', '-created_at']

    fieldsets = (
        ('Project Information', {
            'fields': ('title', 'slug', 'category', 'excerpt', 'description')
        }),
        ('Details', {
            'fields': ('location', 'date_completed', 'beneficiaries')
        }),
        ('Media', {
            'fields': ('image',)
        }),
        ('Display Settings', {
            'fields': ('is_featured', 'is_active', 'order')
        }),
    )


# ==================== GALLERY ADMIN ====================

@admin.register(GalleryCategory)
class GalleryCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'order', 'item_count']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['order', 'name']

    def item_count(self, obj):
        count = obj.items.filter(is_active=True).count()
        return format_html('<b>{}</b> items', count)
    item_count.short_description = "Active Items"


@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'media_type', 'category', 'date_taken', 'is_featured', 'is_active', 'thumbnail_preview']
    list_filter = ['media_type', 'category', 'is_featured', 'is_active']
    search_fields = ['title', 'caption']
    ordering = ['-date_taken', '-created_at']

    fieldsets = (
        ('Item Information', {
            'fields': ('title', 'media_type', 'category', 'caption')
        }),
        ('Media Upload', {
            'fields': ('image', 'video_url'),
            'description': 'Upload a photo, OR paste a video URL for videos. For videos, you can also upload a thumbnail image.'
        }),
        ('Details', {
            'fields': ('date_taken',)
        }),
        ('Display Settings', {
            'fields': ('is_featured', 'is_active', 'order')
        }),
    )

    def thumbnail_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:50px;border-radius:4px;" />', obj.image.url)
        if obj.video_url:
            return format_html('<span style="color:#27ae60;"><i class="fas fa-video"></i> Video</span>')
        return '-'
    thumbnail_preview.short_description = "Preview"


# Customize admin site
admin.site.site_header = "Aunt Enid Campaign Admin"
admin.site.site_title = "Aunt Enid Admin"
admin.site.index_title = "Welcome to Aunt Enid Campaign Administration"