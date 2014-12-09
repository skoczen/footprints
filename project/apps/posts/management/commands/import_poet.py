# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
import codecs
import datetime
import json
from posts.models import Post, Author


def load_from_source(source):
    source = json.loads(source)
    author = Author.objects.get_or_create(public_domain=True, archive=True, archive_name=source["name"])[0]
    author.wikipedia_url = source["wikipedia_url"]
    author.birthdate = datetime.datetime.strptime(source["birthdate"], "%Y-%m-%d")
    author.deathdate = datetime.datetime.strptime(source["deathdate"], "%Y-%m-%d")
    author.save()
    print "Importing the posts of %s:" % author

    for p in source["posts"]:
        post = Post.objects.get_or_create(author=author, public_domain=True, imported=True, title=p["title"])[0]
        print " %s" % post
        post.body = p["body"].replace("  ", "&nbsp;&nbsp;").replace('â€”', "'")
        pub_date = None
        if p["publication_date"]:
            pub_date = datetime.datetime.strptime(p["publication_date"], "%Y-%m-%d")
        post.is_draft = False
        post.published_at = pub_date
        post.written_on = pub_date
        post.started_at = pub_date
        post.show_draft_revisions = False
        post.show_published_revisions = False
        post.approximate_publication_date = p["approximate_publication_date"] or False
        post.source_url = p["source_url"] or None
        post.save(force_longest_line_recalc=True)


class Command(BaseCommand):

    def handle(self, *args, **options):
        if len(args) == 0:
            print "You must provide the name of the file to import"
        f = codecs.open(args[0], "r", "utf-8")
        source = f.read()
        load_from_source(source)
