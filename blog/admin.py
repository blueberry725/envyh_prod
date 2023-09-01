from django.contrib import admin
from import_export.admin import ImportExportMixin
from .models import Category, Tag, Author, Post, SliderFeaturedPost, FeaturedPost
from .resources import PostResource

admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Author)
admin.site.register(SliderFeaturedPost)
admin.site.register(FeaturedPost)

@admin.register(Post)
class PostAdmin(ImportExportMixin, admin.ModelAdmin):
    resource_class = PostResource
