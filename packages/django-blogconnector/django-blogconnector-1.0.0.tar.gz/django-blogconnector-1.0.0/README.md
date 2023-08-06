[![Build Status](https://travis-ci.org/avryhof/django-blogconnector.svg)](https://travis-ci.org/avryhof/django-blogconnector)
[![CodeFactor](https://www.codefactor.io/repository/github/avryhof/django-blogconnector/badge)](https://www.codefactor.io/repository/github/avryhof/django-blogconnector)
[![PyPI - Downloads](https://img.shields.io/pypi/v/django-blogconnector.svg)](https://pypi.org/project/django-blogconnector)
[![PyPI - Downloads](https://img.shields.io/pypi/djversions/django-blogconnector.svg)](https://pypi.org/project/django-blogconnector)


Django-BlogConnector
===================

A very simple app that pulls in Posts, categories and Authors from a Blog's RSS/Atom feed.

Only tested with a WordPress blog so far.  Adding others should be possible.

----------
Installation and Setup
-------------

You can install it easily from pypi by running

    pip install django-blogconnector

After installing the package, add `django_blogconnector` in in your `INSTALLED_APPS` settings

```python
INSTALLED_APPS = (
    ...
    'django_blogconnector',
)
```

After this, you can either include the sample urls in your urls.py.

```python
urlpatterns = [
    ...
    path('blog/', include('django_blogconnector.urls')),
    ...
]
```

or create your own views for blog posts.

There are some template tags to simplify template creation:

```html
{% posts %}  - Render the list of posts with the template at blog_connector/post.html

{% posts <category-slug> %} - Same as posts, but for a single category.

{% categories %} - Renders the category list with the blog_connector/category.html and blog_connector/category_link.html templates.

{% ...|paragraphs:n }% - Renders the first *n* paragraphs of the variable passed into it.
```

Everything has admins, so you can add blogs, edit posts, link blog users to your own users, rename categories, etc.