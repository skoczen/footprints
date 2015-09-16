# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
import codecs
import datetime
import json
import time
import os
import requests
import shutil
from posts.models import Fantastic, Read, Post
from django.conf import settings

FOLDER_ROOT = os.path.abspath(os.path.join(os.getcwd(), "export"))
DAYONE_PATH = "/Users/skoczen/Dropbox/Apps/Day\ One/Journal.dayone/photos/"
print FOLDER_ROOT


def firebase_url(endpoint, shallow=False):
    querystring = False
    if "?" in endpoint:
        querystring = endpoint.split("?")[1]
        endpoint = endpoint.split("?")[0]
    if not endpoint.endswith("/"):
        endpoint = "%s/" % endpoint
    if endpoint.startswith("/"):
        endpoint = endpoint[1:]

    if not querystring:
        url = "https://%s/%s.json?format=export&auth=%s" % (
            settings.FIREBASE_ENDPOINT,
            endpoint,
            settings.FIREBASE_KEY,
        )
    if querystring:
        url = "https://%s/%s.json?%s&format=export&auth=%s" % (
            settings.FIREBASE_ENDPOINT,
            endpoint,
            querystring,
            settings.FIREBASE_KEY,
        )

    if shallow:
        url = "%s&shallow=true" % url

    return url


def firebase_put(endpoint, data, acks_late=True, shallow=False):
    # TODO: get endpoint make sure it hasn't been updated more recently.
    # print(firebase_url(endpoint))
    # print json.dumps(data)
    r = requests.put(firebase_url(endpoint, shallow=shallow), json.dumps(data))
    if not r.status_code == 200:
        print(r.status_code)
        print(r.json())
    assert r.status_code == 200


def firebase_patch(endpoint, data, acks_late=True, shallow=False):
    # TODO: get endpoint make sure it hasn't been updated more recently.
    # print(firebase_url(endpoint, shallow=shallow))
    # print json.dumps(data)
    r = requests.patch(firebase_url(endpoint, shallow=shallow), json.dumps(data))
    if not r.status_code == 200:
        print(r.status_code)
        print(r.json())
    assert r.status_code == 200


def firebase_post(endpoint, data, acks_late=True, shallow=False):
    print json.dumps(data)
    r = requests.post(firebase_url(endpoint, shallow=shallow), json.dumps(data))
    if not r.status_code == 200:
        print(r.status_code)
        print(r.json())
    assert r.status_code == 200
    return r.json()


def firebase_get(endpoint, acks_late=True, shallow=False):
    # r = requests.get(firebase_url(endpoint, shallow=shallow), json.dumps(data))
    r = requests.get(firebase_url(endpoint, shallow=shallow))
    if not r.status_code == 200:
        print(r.status_code)
        print(r.json())
    assert r.status_code == 200
    return r.json()


def firebase_delete(endpoint, acks_late=True, shallow=False):
    # r = requests.delete(firebase_url(endpoint, shallow=shallow), json.dumps(data))
    r = requests.delete(firebase_url(endpoint, shallow=shallow))
    if not r.status_code == 200:
        print(r.status_code)
        print(r.json())
    assert r.status_code == 200
    return r.json()


class Command(BaseCommand):

    def handle(self, *args, **options):

        # class Fantastic(BaseModel):
        #     post = models.ForeignKey(Post)
        #     uuid = models.CharField(max_length=500, blank=True, null=True)
        #     marked_at = models.DateTimeField(auto_now_add=True, editable=False)
        #     on = models.BooleanField(default=True)

        #     reader = models.ForeignKey(Author, blank=True, null=True)

        # class Read(BaseModel):
        #     post = models.ForeignKey(Post)
        #     uuid = models.CharField(max_length=500, blank=True, null=True)
        #     read_at = models.DateTimeField(auto_now_add=True, editable=False)

        #     reader = models.ForeignKey(Author, blank=True, null=True)

        # users
        # ee8ffed1-2b2f-4f23-94d9-ecbe8fb263d5
        #  pieces
        #  deep-breath
        #  test
        #  facebook_shared:
        # true
        #  loved:
        # true
        #  read:
        # true
        #  twitter_shared:
        # true

        # Events:
        # -JyikqB_dgj8i_KNMhnH
        #  timestamp: 1441746084692
        #  type: "read"
        #  uid: "6a4ea007-aed0-4f4e-99a3-7fd1789f13b0"
        #  url: "yep-this-happened-today"


        firebase_delete("/events/")
        firebase_delete("/users/")
        firebase_delete("/pieces/")

        for f in Fantastic.objects.all():
            if f.on:
                if not f.post.is_draft or f.post.allow_private_viewing:
                    uuid = f.uuid
                    if f.reader:
                        uuid = f.reader.pk
                    url = f.post.permalink.lower()
                    if url[-1] == "/":
                        url = url[:-1]
                    if url[0] == "/":
                        url = url[1:]

                    print "/users/%s/pieces/%s/loved" % (uuid, url),
                    firebase_patch(
                        "/users/%s/pieces/%s/" % (uuid, url),
                        {"loved": True}
                    )
                    event = {
                        "timestamp": int(time.mktime(f.marked_at.timetuple()) * 1000),
                        "type": "loved",
                        "uid": uuid,
                        "url": url,
                    }
                    print event
                    resp = firebase_post("/events/", event)
                    firebase_put("/users/%s/events/%s" % (uuid, resp["name"]), event)
                    user_data = {}
                    user_data[uuid] = True
                    firebase_patch("/pieces/%s/loved/" % (url,), user_data)
                    print ".",

        for r in Read.objects.all():
            if not r.post.is_draft or r.post.allow_private_viewing:
                uuid = r.uuid
                if r.reader:
                    uuid = r.reader.pk

                url = r.post.permalink.lower()
                if url[-1] == "/":
                    url = url[:-1]
                if url[0] == "/":
                    url = url[1:]

                firebase_patch(
                    "/users/%s/pieces/%s/" % (uuid, url),
                    {"read": True}
                )
                event = {
                    "timestamp": int(time.mktime(r.read_at.timetuple()) * 1000),
                    "type": "read",
                    "uid": uuid,
                    "url": url
                }
                resp = firebase_post("/events/", event)
                firebase_put("/users/%s/events/%s" % (uuid, resp["name"]), event)
                user_data = {}
                user_data[uuid] = True
                firebase_patch("/pieces/%s/read/" % (url,), user_data)
                print ".",

        for p in Post.objects.all():
            if not p.is_draft or p.allow_private_viewing:
                url = p.permalink.lower()
                if url[-1] == "/":
                    url = url[:-1]
                if url[0] == "/":
                    url = url[1:]

                print("Twitter for %s (%s)" % (p.title, p.num_twitter_activity))
                for i in range(0, p.num_twitter_activity):
                    d = {}
                    d["migrated_%s" % i] = True
                    firebase_patch("/pieces/%s/twitter_shared/" % url, d)
                    print ".",

                print("Facebook for %s (%s)" % (p.title, p.num_facebook_activity))
                for i in range(0, p.num_facebook_activity):
                    d = {}
                    d["migrated_%s" % i] = True
                    firebase_patch("/pieces/%s/facebook_shared/" % url, d)
                    print ".",
