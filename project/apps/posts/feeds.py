import datetime
from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string

from posts.models import Backup, Fantastic, Post, Author, PostRevision, Read, PostImage


class LatestEntriesFeed(Feed):
    
    link = "/sitenews/"
    description = "Ink and Feet"

    def get_object(self, request, post_id):
        print "request"
        print request
        return get_object_or_404(Post, pk=post_id)


    def title(self, obj):
        print obj
        print self
        print self.__dict__
        # print obj.__dict__
        return "Ink and Foots?"

    def items(self):
        return Post.objects.filter(email_publish_intent=True, is_draft=False, written_on__gt=datetime.date.today()-datetime.timedelta(days=30)).order_by('written_on')

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
        return item.full_permalink


    def get_context_data(self, **kwargs):
        print "kwargs"
        print kwargs
        context = super(LatestEntriesFeed, self).get_context_data(**kwargs)
        print context
        # context['foo'] = 'bar'
        return context