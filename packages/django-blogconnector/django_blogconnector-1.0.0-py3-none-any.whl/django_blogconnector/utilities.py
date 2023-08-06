import html

import requests
import xmltodict

from django_blogconnector.models import BlogPost, BlogUser, BlogCategory
from .helpers import to_dict, clean_api_results, format_dates, convert_keys, dict_key_search, make_bool


def read_blog_feed(blog):
    feed_resp = requests.get(blog.syndication_link)
    feed_xml = feed_resp.text

    raw_feed_dict = to_dict(xmltodict.parse(feed_xml))
    clean_feed_dict = clean_api_results(raw_feed_dict)

    feed_dict = format_dates(convert_keys(clean_feed_dict))

    if 'rss' in feed_dict:
        rss_data = feed_dict.get('rss', {}).get('channel')

        for attrib in ['title', 'link', 'description', 'last_build_date', 'language', 'update_period',
                       'update_frequency']:
            if attrib in rss_data:
                attrib_value = rss_data.get(attrib)

            else:
                attrib_value = rss_data.get(dict_key_search(attrib, rss_data))

            setattr(blog, attrib, attrib_value)

            blog.save()

        items = rss_data.get('item')

        for item in items:
            category_id = item.get('category')
            try:
                category = BlogCategory.objects.get(name=category_id)
            except BlogCategory.DoesNotExist:
                category = BlogCategory.objects.create(name=category_id)

            creator_id = item.get(dict_key_search('creator', item))
            try:
                creator = BlogUser.objects.get(blog_username=creator_id)
            except BlogUser.DoesNotExist:
                creator = BlogUser.objects.create(blog_username=creator_id)

            content = html.unescape(item.get(dict_key_search('content', item)))
            description = html.unescape(item.get('description'))

            guid = item.get('guid', {}).get('#text')
            try:
                post = BlogPost.objects.get(guid=guid)

            except BlogPost.DoesNotExist:
                post = BlogPost.objects.create(
                    title=item.get('title'),
                    link=item.get('link'),
                    pub_date=item.get('pub_date'),
                    creator=creator,
                    category=category,
                    description=description,
                    content=content,
                    guid=guid,
                    guid_is_permalink=make_bool(item.get('guid', {}).get('@is_perma_link')),
                    blog_source=blog
                )

            else:
                post.title = item.get('title')
                post.link = item.get('link')
                post.pub_date = item.get('pub_date')
                post.creator = creator
                post.category = category
                post.description = description
                post.content = content
                post.guid_is_permalink = make_bool(item.get('guid', {}).get('@is_perma_link'))
                post.blog_source = blog
                post.save()
