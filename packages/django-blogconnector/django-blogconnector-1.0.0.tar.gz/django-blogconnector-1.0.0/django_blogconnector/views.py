import bleach
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.generic import TemplateView
from past.types import unicode

from django_blogconnector.models import BlogCategory, BlogPost


class BlogHomeView(TemplateView):
    template_name = 'blog_connector/page.html'
    page_title = ''

    def get_context_data(self, **kwargs):
        context = super(BlogHomeView, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['extra_css'] = []
        context['extra_javascript'] = []

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()

        return render(request, self.template_name, context)

    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        return super(BlogHomeView, self).dispatch(*args, **kwargs)


class BlogCategoryView(TemplateView):
    template_name = 'blog_connector/category.html'
    page_title = ''

    def get_context_data(self, **kwargs):
        context = super(BlogCategoryView, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['extra_css'] = []
        context['extra_javascript'] = []

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()

        category_slug = kwargs.get('category_slug')

        if isinstance(category_slug, (str, unicode)):
            category_slug = bleach.clean(category_slug)

            try:
                category = BlogCategory.objects.get(slug=category_slug)

            except BlogCategory.DoesNotExist:
                return redirect('blog_home')

            else:
                context['category'] = category

        return render(request, self.template_name, context)

    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        return super(BlogCategoryView, self).dispatch(*args, **kwargs)


class BlogPostView(TemplateView):
    template_name = 'blog_connector/single.html'
    page_title = ''

    def get_context_data(self, **kwargs):
        context = super(BlogPostView, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['extra_css'] = []
        context['extra_javascript'] = []

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()

        post_slug = kwargs.get('post_slug')

        if isinstance(post_slug, (str, unicode)):
            post_slug = bleach.clean(post_slug)

            try:
                post = BlogPost.objects.get(slug=post_slug)

            except BlogPost.DoesNotExist:
                return redirect('blog_home')

            else:
                context['post'] = post

        return render(request, self.template_name, context)

    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        return super(BlogPostView, self).dispatch(*args, **kwargs)