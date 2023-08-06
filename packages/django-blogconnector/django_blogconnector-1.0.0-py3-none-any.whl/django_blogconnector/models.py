from django.conf import settings
from django.db import models
from django.db.models import DO_NOTHING
from django.utils.encoding import python_2_unicode_compatible
from django.utils.text import slugify


@python_2_unicode_compatible
class BlogSource(models.Model):
    enabled = models.BooleanField(default=True)
    title = models.CharField(max_length=200, blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    syndication_type = models.CharField(max_length=16, blank=True, null=True)
    syndication_link = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    last_build_date = models.DateTimeField(blank=True, null=True)
    language = models.CharField(max_length=20, blank=True, null=True, default=settings.LANGUAGE_CODE)
    update_period = models.CharField(max_length=20, blank=True, null=True, default='hourly')
    update_frequency = models.CharField(max_length=8, blank=True, null=True, default='1')
    blog_type = models.CharField(max_length=100, blank=True, null=True, default='WordPress')

    class Meta:
        verbose_name = 'Blog'
        verbose_name_plural = 'Blogs'

    def __str__(self):
        return self.title if self.title else 'Blog'


@python_2_unicode_compatible
class BlogCategory(models.Model):
    enabled = models.BooleanField(default=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    slug = models.SlugField(max_length=200, blank=True, null=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name if self.name else 'Blog Category'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super(BlogCategory, self).save(*args, **kwargs)


@python_2_unicode_compatible
class BlogUser(models.Model):
    enabled = models.BooleanField(default=True)
    blog_username = models.CharField(max_length=100, blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=DO_NOTHING)

    class Meta:
        verbose_name = 'Blog User'
        verbose_name_plural = 'Blog Users'

    def __str__(self):
        return self.blog_username if self.blog_username else 'Blog User'


@python_2_unicode_compatible
class BlogPost(models.Model):
    enabled = models.BooleanField(default=True)
    title = models.CharField(max_length=200, blank=True, null=True)
    slug = models.SlugField(max_length=200, blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    pub_date = models.DateTimeField(blank=True, null=True)
    creator = models.ForeignKey(BlogUser, blank=True, null=True, on_delete=DO_NOTHING)
    category = models.ForeignKey(BlogCategory, blank=True, null=True, on_delete=DO_NOTHING)
    description = models.TextField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    guid = models.CharField(max_length=255, blank=True, null=True)
    guid_is_permalink = models.BooleanField(default=False)
    blog_source = models.ForeignKey(BlogSource, blank=True, null=True, on_delete=DO_NOTHING)

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def __str__(self):
        return self.title if self.title else 'Blog Post'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        super(BlogPost, self).save(*args, **kwargs)
