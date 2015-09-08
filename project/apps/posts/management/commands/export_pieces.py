# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
import codecs
import datetime
import json
import os
import requests
import shutil
from posts.models import Post, Author

FOLDER_ROOT = os.path.abspath(os.path.join(os.getcwd(), "export"))
DAYONE_PATH = "/Users/skoczen/Dropbox/Apps/Day\ One/Journal.dayone/photos/"
print FOLDER_ROOT


class Command(BaseCommand):

    def handle(self, *args, **options):
        for p in Post.objects.all():
            # Folder.
            if p.permalink and p.is_draft == False:
                lower_path = p.permalink.lower()
                if lower_path[0] == "/":
                    lower_path = lower_path[1:]

                folder = "%s/%s" % (FOLDER_ROOT, lower_path)
                print p.title

                if not os.path.exists(folder):
                    print folder
                    os.makedirs(folder)

                # Piece.md
                with open(os.path.join(folder, "piece.md"), "w+") as f:
                    f.write(p.body.encode("utf-8"))
                    print "  - Piece"

                # Header.jpg
                # If we can get it locally full-res, do it.  Otherwise,
                found = False
                if p.dayone_image:
                    print "  - Image ",
                    if len(p.dayone_image.name) == 90:
                        combined = os.path.join(DAYONE_PATH, "%s.jpg" % p.dayone_image.name[14:46]).replace("\ ", " ")
                        if os.path.exists(combined):
                            shutil.copyfile(
                                combined,
                                os.path.join(folder, "header.jpg"),
                            )
                            print "Found locally."
                            found = True

                    if not found:
                        if os.path.exists(os.path.join(folder, "header.jpg")):
                            print "Downloaded."
                        else:
                            url = p.dayone_image_url.replace(".com/", ".com/dayone_images/")
                            print "Downloading  %s..." % url

                            r = requests.get(url)
                            with open(os.path.join(folder, "header.jpg"), "w+") as f:
                                f.write(r.content)

                print "  - Meta "
                with open(os.path.join(folder, "meta.yml"), "w+") as f:
                    f.write(
"""url: %(url)s
title: "%(title)s"
description: "%(description)s"
header_image: header.jpg

post_num: %(pk)s
published: true
published_date: "%(published_date)s"
updated_date: "%(updated_date)s"
related_piece_1: %(related_piece_1)s
related_piece_2: %(related_piece_2)s
related_piece_3: %(related_piece_3)s
""".encode("utf-8") % {
    "url": lower_path.encode("utf-8"),
    "title": p.title.encode("utf-8").replace('’', "'").replace('"', '\\"').replace("\n", "\\n").replace("\r", ""),
    "description": p.description.replace("\n", "\\n").replace("\r", "").encode("utf-8").replace('’', "'").replace('"', '\\"'),
    "pk": p.pk,
    "published_date": p.published_at.strftime("%Y-%m-%d %H:%M"),
    "updated_date": p.updated_at.strftime("%Y-%m-%d %H:%M"),
    "related_piece_1": "",
    "related_piece_2": "",
    "related_piece_3": "",
})

                print "  - Social "
                with open(os.path.join(folder, "social.yml"), "w+") as f:
                    f.write(
"""start_date: %(start_date)s
posts:
    - twitter:
        publication_plus_days: 0
        content: "%(tweet)s"
        time: "%(time)s"
        image: header.jpg
    - facebook:
        publication_plus_days: 0
        content: "%(post)s"
        time: "%(time)s"
        image: header.jpg
""" % {
    "start_date": p.published_at.strftime("%Y-%m-%d"),
    "tweet": p.twitter_status_text.encode("utf-8").replace('’', "'").replace('"', '\\"').replace("\n", "\\n").replace("\r", ""),
    "time": p.published_at.strftime("%H:%M"),
    "post": p.facebook_status_text.encode("utf-8").replace('’', "'").replace('"', '\\"').replace("\n", "\\n").replace("\r", ""),
})
