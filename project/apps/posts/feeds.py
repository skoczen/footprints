import datetime
from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string

from posts.models import Backup, Fantastic, Post, Author, PostRevision, Read, PostImage


class LatestEntriesFeed(Feed):
    # title = "Police beat site news"
    link = "/sitenews/"
    description = "Updates on changes and additions to police beat central."

    def title(self, obj):
        print obj
        return "Ink and Foots?"

    def items(self):
        return Post.objects.filter(is_draft=False, written_on__gt=datetime.date.today()-datetime.timedelta(days=30)).order_by('-written_on')

    def item_title(self, item):
        return item.title_html

    def item_description(self, item):
        html = ""
        if item.dayone_image:
            html += "<img src='%s'/>" % item.dayone_image.url
        html += item.body_html
        return html

    # item_link is only needed if NewsItem has no get_absolute_url method.
    def item_link(self, item):
        return reverse('posts:post', args=[item.pk])


    def get_context_data(self, **kwargs):
        context = super(LatestEntriesFeed, self).get_context_data(**kwargs)
        print context
        # context['foo'] = 'bar'
        return context