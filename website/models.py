from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify
from .image_utils import compress_image_field


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
        # Auto-compress uploaded images so they load fast
        compress_image_field(self.featured_image)

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

    # About Section - fully editable from admin
    about_title = models.CharField(max_length=100, default="Who is Aunt Enid?")
    about_subtitle = models.CharField(max_length=200, default="A dedicated community leader with a heart for service and transformation")

    about_part1_title = models.CharField(
        max_length=100, default="Why I'm Running",
        help_text="Heading for the first About section"
    )
    about_part1_text = models.TextField(
        default="As a woman leader deeply rooted in Kabale District, I believe in the power of inclusive governance that uplifts every voice, especially those often unheard. Our community deserves leadership that understands the unique challenges we face and has the compassion to address them with wisdom and determination.",
        help_text="Content for the first About section"
    )
    about_part2_title = models.CharField(
        max_length=100, default="My Vision",
        help_text="Heading for the second About section"
    )
    about_part2_text = models.TextField(
        default="I envision a Kabale District where every family thrives, where women and youth are empowered, where education is accessible to all, and where our natural resources benefit our entire community. This vision drives my commitment to serve as your representative in Parliament.",
        help_text="Content for the second About section"
    )

    # Legacy fields kept for DB compatibility (hidden from admin)
    why_running = models.TextField(default="As a woman leader deeply rooted in Kabale District...", editable=False)
    vision = models.TextField(default="I envision a Kabale District where every family thrives...", editable=False)

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


# ==================== IMPACT SECTION ====================

class ProjectCategory(models.Model):
    """Dynamic categories for Impact Projects - fully manageable from admin"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True, help_text="Optional short description of this category")
    icon = models.CharField(
        max_length=50, default="hands-helping",
        help_text="FontAwesome icon class e.g. 'hands-helping', 'female', 'seedling', 'heartbeat'"
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Project Category"
        verbose_name_plural = "Project Categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('website:impact_category', kwargs={'slug': self.slug})


class ImpactProject(models.Model):
    """Model for community development / impact projects"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    category = models.ForeignKey(
        ProjectCategory, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='projects', help_text="Select the category for this project"
    )
    excerpt = models.TextField(max_length=400, help_text="Short description shown on the listing page")
    description = models.TextField(help_text="Full project description and story")
    image = models.ImageField(upload_to='impact/', blank=True, null=True, help_text="Main project photo")
    location = models.CharField(max_length=150, default="Kabale District")
    date_completed = models.DateField(null=True, blank=True, help_text="Leave blank if ongoing")
    beneficiaries = models.CharField(max_length=200, blank=True, help_text="e.g. '200 women trained'")
    is_featured = models.BooleanField(default=False, help_text="Show on homepage impact highlights")
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_completed', '-created_at']
        verbose_name = "Impact Project"
        verbose_name_plural = "Impact Projects"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
        # Auto-compress uploaded images so they load fast
        compress_image_field(self.image)

    def get_absolute_url(self):
        return reverse('website:impact_detail', kwargs={'slug': self.slug})


# ==================== GALLERY / MEDIA SECTION ====================

class GalleryCategory(models.Model):
    """Dynamic categories for Gallery Items - fully manageable from admin"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Gallery Category"
        verbose_name_plural = "Gallery Categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class GalleryItem(models.Model):
    """Model for campaign photos and videos with social sharing.
    Supports three video sources:
      1. Uploaded video file (mp4/mov/webm from phone or laptop)
      2. YouTube / Vimeo URL  → embedded in iframe
      3. TikTok / Facebook / other URL → opens on the platform
    """
    MEDIA_TYPE_CHOICES = [
        ('image', 'Photo'),
        ('video', 'Video'),
    ]

    title = models.CharField(max_length=200)
    media_type = models.CharField(
        max_length=10, choices=MEDIA_TYPE_CHOICES, default='image',
        help_text="Select 'Photo' for an image, 'Video' for a video file or link."
    )
    image = models.ImageField(
        upload_to='gallery/images/', blank=True, null=True,
        help_text="Upload a photo (or a thumbnail for videos uploaded by URL)."
    )
    # ---- Direct video file upload (phone/laptop) ----
    video_file = models.FileField(
        upload_to='gallery/videos/', blank=True, null=True,
        help_text=(
            "Upload a video directly from your phone or laptop (MP4, MOV, WebM, AVI — max 200 MB). "
            "Leave blank if you are using a video link below instead."
        )
    )
    # ---- External video link ----
    video_url = models.URLField(
        blank=True,
        help_text=(
            "OR paste a YouTube, Vimeo, TikTok, or Facebook video link. "
            "Leave blank if you uploaded a video file above."
        )
    )
    caption = models.TextField(blank=True, help_text="Optional caption shown under the media.")
    category = models.ForeignKey(
        GalleryCategory, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='items', help_text="Select the gallery category."
    )
    date_taken = models.DateField(null=True, blank=True, help_text="Date the photo/video was taken.")
    is_featured = models.BooleanField(default=False, help_text="Feature on gallery landing page.")
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_taken', '-created_at']
        verbose_name = "Gallery Item"
        verbose_name_plural = "Gallery Items"

    def __str__(self):
        return self.title

    @property
    def video_file_url(self):
        """Return the URL of the uploaded video file, or empty string."""
        if self.video_file and hasattr(self.video_file, 'url'):
            return self.video_file.url
        return ''

    def embed_url(self):
        """Return an embeddable iframe src for YouTube/Vimeo, else return the raw URL."""
        import re
        url = self.video_url or ''
        yt = re.search(r'(?:youtube\.com/watch\?v=|youtu\.be/)([A-Za-z0-9_-]{11})', url)
        if yt:
            return f"https://www.youtube.com/embed/{yt.group(1)}?autoplay=1"
        vm = re.search(r'vimeo\.com/(\d+)', url)
        if vm:
            return f"https://player.vimeo.com/video/{vm.group(1)}?autoplay=1"
        return url

    def video_source_type(self):
        """Return 'file', 'embed', or 'external' to guide the template/lightbox."""
        if self.video_file:
            return 'file'
        import re
        url = self.video_url or ''
        if re.search(r'youtube\.com|youtu\.be|vimeo\.com', url):
            return 'embed'
        if url:
            return 'external'
        return ''

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Compress the thumbnail/photo image (never the video_file itself)
        compress_image_field(self.image)