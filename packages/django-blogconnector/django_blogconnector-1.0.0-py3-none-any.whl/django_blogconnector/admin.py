from django.contrib import admin

from .models import BlogSource, BlogCategory, BlogUser, BlogPost


@admin.register(BlogSource)
class BlogSourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'last_build_date', 'enabled',)
    list_filter = ('enabled', 'blog_type', 'syndication_type')
    search_fields = ('title',)


@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'enabled',)
    list_filter = ('enabled',)
    search_fields = ('name',)


@admin.register(BlogUser)
class BlogUserAdmin(admin.ModelAdmin):
    list_display = ('blog_username', 'user', 'enabled',)
    list_filter = ('enabled',)
    search_fields = ('blog_username',)


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'pub_date', 'enabled',)
    list_filter = ('enabled', 'creator', 'category', 'blog_source')
    search_fields = ('title', 'description', 'content', 'creator', 'category', 'blog_source')
