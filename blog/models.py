from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from PIL import Image, ImageOps
import os
from django.conf import settings

# Category Model
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name

# Tag Model
class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

# Author Model
class Author(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField()
    email = models.EmailField()

    def __str__(self):
        return self.name

# Post Model
class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = RichTextUploadingField()
    description = models.TextField(null=True, blank=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_images/', null=True, blank=True)
    thumbnail_mini = models.ImageField(upload_to='thumbnail_mini', blank=True)
    thumbnail_small = models.ImageField(upload_to='thumbnail_small', blank=True)
    thumbnail_medium = models.ImageField(upload_to='thumbnail_medium', blank=True)
    thumbnail_large = models.ImageField(upload_to='thumbnail_large', blank=True)

    is_active = models.BooleanField(default=True)

    # SEO fields
    meta_title = models.CharField(max_length=200, help_text="Meta title for SEO")
    meta_description = models.TextField(help_text="Meta description for SEO")
    meta_keywords = models.CharField(max_length=250, help_text="Meta keywords for SEO (comma-separated)")
    canonical_url = models.URLField(max_length=255, blank=True, help_text="Canonical URL for SEO")

    # Image thumbnail creation
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.thumbnail_small:  # Check the correct field name
            self.create_thumbnails()

    def create_thumbnails(self):
        if not self.image:
            return

        img = Image.open(self.image.path)

        # Define thumbnail sizes and corresponding names
        thumbnail_sizes = [
            (90, 80, 'thumbnail_mini'),
            (530, 504, 'thumbnail_small'),
            (900, 504, 'thumbnail_medium'),
            (1169, 600, 'thumbnail_large'),
            (690, 654, 'thumbnail_square'),
            # Add more sizes as needed
        ]

        for width, height, field_name in thumbnail_sizes:
            thumb_img = ImageOps.fit(img, (width, height), method=0, bleed=0.0, centering=(0.5, 0.5))
            # Construct the thumbnail path using the MEDIA_ROOT and upload_to
            thumbnail_path = os.path.join(settings.MEDIA_ROOT, self._meta.get_field(field_name).upload_to,
                                          self.image.name)
            thumb_img.save(thumbnail_path)
            setattr(self, field_name, thumbnail_path.replace(settings.MEDIA_ROOT, ''))

        self.save()

    def __str__(self):
        return self.title

# SliderFeaturedPost Model
class SliderFeaturedPost(models.Model):
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0, help_text='Order in which the post appears in the slider')
    is_active = models.BooleanField(default=True, help_text='Whether the post is active in the slider')

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.post.title} - Slider Featured Order: {self.order}"

# FeaturedPost Model
class FeaturedPost(models.Model):
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0, help_text='Order in which the post appears in the slider')
    is_active = models.BooleanField(default=True, help_text='Whether the post is active in the slider')

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.post.title} - Slider Featured Order: {self.order}"
