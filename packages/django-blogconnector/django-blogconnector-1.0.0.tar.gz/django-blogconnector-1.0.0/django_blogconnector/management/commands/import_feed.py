import random

from django.core.management import BaseCommand

from django_blogconnector.models import BlogSource
from django_blogconnector.utilities import read_blog_feed


class Command(BaseCommand):
    help = 'Help goes here.'
    verbosity = 0
    current_file = None
    log_file_name = None
    log_file = False

    def handle(self, *args, **options):
        self.verbosity = int(options['verbosity'])

        blogs = BlogSource.objects.filter(enabled=True)

        for blog in blogs:
            read_blog_feed(blog)
