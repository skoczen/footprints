import datetime
import json
import pytz
import re
import random
import uuid

from dropbox.client import DropboxOAuth2Flow, DropboxClient
from facepy import GraphAPI
import tweepy
from requests_oauth2 import OAuth2

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.core.cache import cache
from django.db.models import Count
from django.db.models import Max, Min
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.template.loader import render_to_string
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.utils import feedgenerator
from annoying.decorators import render_to, ajax_request
from posts.models import Backup, Fantastic, Post, Author, PostRevision, Read, PostImage, Redirect
from posts.forms import AccountForm, FantasticForm, PostForm, ReadForm, SocialShareForm, BlogForm, BlogUserForm
from posts.tasks import generate_backup_zip, sync_posts
from posts.social import twitter_auth, authorized_tweepy_api, facebook_auth, authorized_facebook_api

POSTS_PER_PAGINATION = 10


@render_to("posts/home.html")
def home(request):
    return locals()

@render_to("posts/explore.html")
def explore(request):
    # Yeah, I know.  I'll move this to a cached, non-db killing thing once we've got a few people.
    num_posts = Post.objects.filter(is_draft=False).count()
    recent_reads = Read.objects.all().order_by("-read_at")[:5]
    recent_published = Post.objects.filter(is_draft=False).order_by("-sort_datetime")[:5]
    active_authors = Author.objects.all().annotate(latest_update=Max('post__sort_datetime')).order_by("-latest_update")[:5]
    most_favorited = Post.objects.all().annotate(number_fantastics=Count('fantastic')).order_by("-number_fantastics")[:5]
    
    top_classics = Post.objects.filter(public_domain=True).order_by("?")[:5]
    great_authors = Author.objects.filter(public_domain=True).order_by("?")[:5]
    return locals()


@render_to("posts/my_reading.html")
@login_required
def my_reading(request):
    my_reads = Read.objects.filter(reader=request.user.get_profile()).select_related().order_by("-read_at")
    # .annotate(Min('read_at')).distinct("post")
    return locals()


@render_to("posts/backups.html")
@login_required
def my_backups(request):
    backups = Backup.objects.filter(author=request.user.get_profile())
    return locals()


@login_required
def generate_backup(request):
    generate_backup_zip(request.user.get_profile().pk)
    # Enable when it's slow/big enough to pay for it.
    # generate_backup_zip.delay(request.user.get_profile())
    return HttpResponseRedirect(reverse("posts:my_backups"))


@render_to("posts/my_account.html")
@login_required
def my_account(request):
    me = request.user
    author = me.get_profile()
    changes_saved = False
    if request.method == "POST":
        form = AccountForm(request.POST, instance=me)
        if form.is_valid():
            me = form.save()
            changes_saved = True

    else:
        form = AccountForm(instance=me)
    return locals()


@render_to("posts/blog_settings.html")
@login_required
def blog_settings(request):
    me = request.user
    author = me.get_profile()
    changes_saved = False
    if request.method == "POST":
        form = BlogForm(request.POST, instance=author)
        user_form = BlogUserForm(request.POST, instance=request.user, prefix="USER")
        if form.is_valid() and user_form.is_valid():
            me = form.save()
            user_form.save()
            redirects = json.loads(form.cleaned_data["redirects"])["data"]
            current_pks = []
            for redirect in redirects:
                if redirect[0] or redirect[1]:
                    if redirect[1] and redirect[1][0] != "/":
                        redirect[1] = "/%s" % redirect[1]
                    if redirect[0] and redirect[0][0] != "/":
                        redirect[0] = "/%s" % redirect[0]
                    r = Redirect.objects.get_or_create(author=author, old_url=redirect[0], new_url=redirect[1])[0]
                    current_pks.append(r.pk)                

            # I hate __ins, but it should be ok for this super rare, limited size query.  Hopefully.
            Redirect.objects.filter(author=author).exclude(pk__in=current_pks).delete()
            changes_saved = True

    else:
        form = BlogForm(instance=author)
        user_form = BlogUserForm(instance=request.user, prefix="USER")
    return locals()


@render_to("posts/author.html")
@login_required
def my_writing(request, author=None):
    author = request.user.get_profile()
    is_me = True
    posts = Post.objects.filter(author=author).order_by("-written_on", "title")
    return locals()

@render_to("posts/author.html")
@login_required
def my_published(request, author=None):
    author = request.user.get_profile()
    is_me = True
    posts = Post.objects.filter(is_draft=False, author=author).order_by("-written_on", "title")
    return locals()


@render_to("posts/author.html")
@login_required
def my_drafts(request, author=None):
    author = request.user.get_profile()
    is_me = True
    posts = Post.objects.filter(is_draft=True, author=author).order_by("-written_on", "title")
    return locals()


@render_to("posts/author.html")
@login_required
def my_prospects(request, author=None):
    author = request.user.get_profile()
    is_me = True
    posts = Post.objects.filter(is_draft=True, prospect=True, author=author).order_by("-written_on", "title")
    return locals()


def get_author_from_domain(request):
    domain = request.get_host()
    if domain[:4] == "www.":
        domain = domain[":4"]
    domain = Author.objects.get(blog_domain__iexact=domain)
    return domain

def get_related_posts(post):
    try:
        top = Post.objects.exclude(dayone_image=None).exclude(dayone_image="").filter(author=post.author, is_draft=False).annotate(fantastics=Count('fantastic')).order_by('-fantastics')[:6]
        random_selection = Post.objects.exclude(dayone_image=None).exclude(dayone_image="").filter(author=post.author, is_draft=False).order_by("?")[:2]
        recent = Post.objects.exclude(dayone_image=None).exclude(dayone_image="").filter(author=post.author, is_draft=False).order_by("-written_on")[:4]
        options = []
        for t in top:
            if t not in options and t.pk != post.pk:
                options.append(t)
        for r in random_selection:
            if r not in options and r.pk != post.pk:
                options.append(r)
        for r in recent:
            if r not in options and r.pk != post.pk:
                options.append(r)

        return random.sample(options, 3)
    except:
        import traceback; traceback.print_exc();

    return []

# def get_related_posts(post):
#     try:
#         top = Post.objects.filter(author=post.author, is_draft=False).exclude(pk=post.pk).annotate(fantastics=Count('fantastic')).order_by('-fantastics')[:6]
#         random_selection = Post.objects.filter(author=post.author, is_draft=False).exclude(pk__in=[post.pk]+[t.pk for t in top]).order_by("?")[:2]
#         options = []
#         for t in top:
#             options.append(t)
#         for r in random_selection:
#             options.append(r)

#         return random.sample(options, 3)
#     except:
#         import traceback; traceback.print_exc();

#     return []

@render_to("posts/blog.html")
def blog(request):
    try:
        fantastic_form = FantasticForm()
        on_blog = True
        author = get_author_from_domain(request)
        # posts = Post.objects.filter(author=author, is_draft=False).order_by("-written_on", "title")[:POSTS_PER_PAGINATION]
        # posts = next_10_annotated_posts_and_forms(author, request)
        posts = author.published_posts[:POSTS_PER_PAGINATION]
        if len(posts) > 0:
            last_timestamp = posts[len(posts)-1].written_on.strftime("%s")
        else:
            last_timestamp = False
        if author.user == request.user:
            is_me = True

        return locals()
    except:
        import traceback; traceback.print_exc();
        from main_site.views import home
        return home(request)
        # pass

@render_to("posts/post.html")
def post(request, title=None):
    author = None
    fantastic_form = FantasticForm()
    try:
        author = get_author_from_domain(request)
    except:
        if request.user.is_authenticated():
            try:
                author = request.user.get_profile()
            except:
                pass

    if not author:
        return HttpResponseRedirect(reverse("posts:home"))

    if Post.objects.filter(slug__iexact=title, author=author).count() == 0 and Post.objects.filter(permalink_path__iexact="/%s" % title, author=author).count() == 0:
        # print request.path
        for r in Redirect.objects.filter(author=author):
            if re.match("%s" % r.old_url, request.path) or re.match(r"%s" % r.old_url, request.path, flags=re.IGNORECASE):
                # print "matched: %s" % r.new_url
                return HttpResponseRedirect(r.new_url)

        return HttpResponseRedirect(reverse("posts:home"))

    if Post.objects.filter(slug__iexact=title, author=author).count() > 0:
        post = Post.objects.get(slug__iexact=title, author=author)
    else:
        post = Post.objects.get(permalink_path__iexact="/%s" % title, author=author)

    related_posts = get_related_posts(post)
    # print related_posts
    is_mine = post.author.user == request.user

    if not request.user.is_authenticated():
        if "uuid" not in request.session:
            request.session["uuid"] = uuid.uuid1()

    if not is_mine and post.is_draft and not post.allow_private_viewing:
        raise Http404("Post not found. Maybe it never existed, or maybe it's a draft and you're not logged in!")

    if is_mine:
        form = PostForm(instance=post)
    else:
        read_form = ReadForm()

        read = None
        fantastic = None
        if not is_mine:
            if request.user.is_authenticated():
                try:
                    read = Read.objects.filter(post=post, reader=request.user.get_profile()).order_by("-read_at")[0]
                except IndexError:
                    pass
                try:
                    fantastic = Fantastic.objects.filter(post=post, reader=request.user.get_profile()).order_by("-marked_at")[0]
                except IndexError:
                    pass
            else:
                if "uuid" in request.session:
                    try:
                        read = Read.objects.filter(post=post, uuid=request.session["uuid"]).order_by("-read_at")[0]
                    except IndexError:
                        pass
                    try:
                        fantastic = Fantastic.objects.filter(post=post, uuid=request.session["uuid"]).order_by("-marked_at")[0]
                    except IndexError:
                        pass
    return locals()

@render_to("posts/edit.html")
def edit(request, title=None):
    try:
        author = get_author_from_domain(request)
    except:
        if request.user.is_authenticated():
            author = request.user.get_profile()

    if not request.user.is_authenticated():
        if "uuid" not in request.session:
            request.session["uuid"] = uuid.uuid1()
    post = Post.objects.get(slug__iexact=title, author=author)
    is_mine = post.author.user == request.user

    if not is_mine and post.is_draft:
        raise Http404("Post not found. Maybe it never was, maybe it's a draft and you're not logged in!")

    if is_mine:
        form = PostForm(instance=post)
    else:
        fantastic_form = FantasticForm()
        read_form = ReadForm()

        read = None
        fantastic = None
        if not is_mine:
            if request.user.is_authenticated():
                try:
                    read = Read.objects.filter(post=post, reader=request.user.get_profile()).order_by("-read_at")[0]
                except IndexError:
                    pass
                try:
                    fantastic = Fantastic.objects.filter(post=post, reader=request.user.get_profile()).order_by("-marked_at")[0]
                except IndexError:
                    pass
            else:
                if "uuid" in request.session:
                    try:
                        read = Read.objects.filter(post=post, uuid=request.session["uuid"]).order_by("-read_at")[0]
                    except IndexError:
                        pass
                    try:
                        fantastic = Fantastic.objects.filter(post=post, uuid=request.session["uuid"]).order_by("-marked_at")[0]
                    except IndexError:
                        pass
    return locals()


@ajax_request
def save_revision(request, author=None, title=None):
    post = Post.objects.get(slug__iexact=title, author__slug__iexact=author)
    new_url = reverse("posts:post", args=(post.slug,))
    old_slug = post.slug
    was_published = not post.is_draft
    is_mine = post.author.user == request.user
    if not is_mine:
        raise Exception("Either this isn't your post, or you're not logged in!")

    success = False
    form = PostForm(request.POST, request.FILES, instance=post)
    if form.is_valid():
        new_post = form.save()
        success = True
        if old_slug != new_post.slug or not was_published and not new_post.is_draft:
            new_url = reverse("posts:post", args=(new_post.slug,))
    else:
        print form

    ret = {"success": success, "new_url": new_url}
    return ret


@render_to("posts/revisions.html")
def revisions(request, author=None, title=None):
    post = Post.objects.get(slug__iexact=title, author__slug__iexact=author)
    is_mine = post.author.user == request.user
    if is_mine:
        revisions = post.revisions

    return locals()


@render_to("posts/revision.html")
def revision(request, author=None, pk=None):
    post = PostRevision.objects.get(pk=pk, author__slug__iexact=author)
    is_mine = post.author.user == request.user
    if (is_mine or
            (post.is_draft and post.post.show_draft_revisions) or
            (not post.is_draft and post.post.show_published_revisions)):
        pass
    else:
        return HttpResponseRedirect(reverse("posts:post", args=(post.post.slug,) ))

    return locals()


def revert_revision(request, pk=None):
    revision = PostRevision.objects.get(pk=pk, author__slug__iexact=request.user.get_profile().slug)
    post = revision.post
    post.body = revision.body
    post.title = revision.title
    post.save()

    return HttpResponseRedirect(reverse("posts:revisions", args=(post.author.slug, post.slug,) ))

def new(request):
    author = Author.objects.get(user=request.user)
    post = Post.objects.create(author=author)
    return HttpResponseRedirect("%s?editing=true" % reverse("posts:edit", args=(post.slug,)))


@ajax_request
def toggle_prospect(request, post_id):
    try:
        post = Post.objects.get(pk=post_id, author=request.user.get_profile())
        post.prospect = not post.prospect
        post.save()
        return {
            "success": True,
            "prospect": post.prospect,
            "pk": post.pk,
        }
    except:
        import traceback; traceback.print_exc();
        pass

    return {"success": False}

@ajax_request
def toggle_featured(request, post_id):
    try:
        post = Post.objects.get(pk=post_id, author=request.user.get_profile())
        post.featured = not post.featured
        post.save()
        return {
            "success": True,
            "featured": post.featured,
            "pk": post.pk,
        }
    except:
        import traceback; traceback.print_exc();
        pass

    return {"success": False}


@ajax_request
def this_was_fantastic(request, post_id):
    post = Post.objects.get(pk=post_id)

    fantastic_form = FantasticForm(request.POST)
    if fantastic_form.is_valid():
        if request.user.is_authenticated():
            fantastic = Fantastic.objects.get_or_create(post=post, reader=request.user.get_profile())[0]
        else:
            if not "uuid" in request.session:
                request.session["uuid"] = uuid.uuid1()
            fantastic = Fantastic.objects.get_or_create(post=post, uuid=request.session["uuid"])[0]

        fantastic.on = fantastic_form.cleaned_data["on"]
        fantastic.save()

        post = Post.objects.get(pk=post_id)
        return {"success": True, "num_people": post.num_fantastics, "post_id": post.pk}

    return {"success": False}


@ajax_request
def mark_read(request, post_id):

    post = Post.objects.get(pk=post_id)
    read_form = ReadForm(request.POST)
    if read_form.is_valid():
        read = read_form.save(commit=False)
        read.post = post
        if request.user.is_authenticated():
            read.reader = request.user.get_profile()
        else:
            if "uuid" in request.session:
                read.uuid = request.session["uuid"]
            read.reader = None
        read.save()

    return {"success": True, "num_reads": post.num_reads}

def next_10_annotated_posts_and_forms(author, request, last_timestamp=None):
    if last_timestamp:
        posts = author.published_posts.filter(written_on__lt=last_timestamp)[:POSTS_PER_PAGINATION]
    else:
        posts = author.published_posts[:POSTS_PER_PAGINATION]

    if not request.user.is_authenticated():
        if "uuid" not in request.session:
            request.session["uuid"] = uuid.uuid1()

    is_mine = author == request.user.get_profile()

    for p in posts:
        # TODO: pull this form for me, actually.
        fantastic_form = FantasticForm()
        read_form = ReadForm()

        read = None
        fantastic = None
        # if not is_mine:
        if request.user.is_authenticated():
            try:
                read = Read.objects.filter(post=post, reader=request.user.get_profile()).order_by("-read_at")[0]
            except IndexError:
                pass
            try:
                post.fantastic = Fantastic.objects.filter(post=post, reader=request.user.get_profile()).order_by("-marked_at")[0]
            except IndexError:
                pass
        else:
            if "uuid" in request.session:
                try:
                    read = Read.objects.filter(post=post, uuid=request.session["uuid"]).order_by("-read_at")[0]
                except IndexError:
                    pass
                try:
                    post.fantastic = Fantastic.objects.filter(post=post, uuid=request.session["uuid"]).order_by("-marked_at")[0]
                except IndexError:
                    pass


@render_to("posts/blog.html")
@login_required
def my_blog(request, author=None):
    fantastic_form = FantasticForm()
    is_me = False
    is_mine = False
    on_blog = True
    author = request.user.get_profile()
    if request.user.get_profile() == author:
        is_me = True
        is_mine = True
    posts = author.published_posts[:POSTS_PER_PAGINATION]
    if len(posts) > 0:
        last_timestamp = posts[len(posts)-1].written_on.strftime("%s")
    else:
        last_timestamp = False
    return locals()

# @render_to("posts/blog.html")
# def blog(request, author=None):
#     if not request.user.is_authenticated():
#         if "uuid" not in request.session:
#             request.session["uuid"] = uuid.uuid1()
#     fantastic_form = FantasticForm()
#     author = Author.objects.get(slug__iexact=author)
#     posts = author.published_posts[:POSTS_PER_PAGINATION]
#     last_timestamp = posts[len(posts)-1].written_on.strftime("%s")
#     return locals()


@login_required
@render_to("posts/social_share.html")
def social_share(request, post_id):
    changes_saved = False
    published = False
    try:
        post = Post.objects.get(pk=post_id)
        assert post.author == request.user.get_profile()
        if request.method == "POST":
            form = SocialShareForm(request.POST, instance=post)
            social_shares_customized = False
            
            if form.is_valid():
                old_post = Post.objects.get(pk=post_id)
                if form.cleaned_data["facebook_status_text"] != old_post.facebook_status_text or\
                    form.cleaned_data["twitter_status_text"] != old_post.twitter_status_text:
                        social_shares_customized = True
                post = form.save()
                if social_shares_customized:
                    post.social_shares_customized = True
                    post.facebook_status_text = form.cleaned_data["facebook_status_text"]
                    post.twitter_status_text = form.cleaned_data["twitter_status_text"]
                    post.save()
                changes_saved = True

                if form.cleaned_data["publish_now"]:
                    if post.twitter_publish_intent:
                        twitter_api = authorized_tweepy_api(post.author)
                        
                        if post.twitter_include_image:
                            resp = twitter_api.update_with_media(post.dayone_image.name, status=post.twitter_status_text, file=post.dayone_image)
                        else:
                            resp = twitter_api.update_status(post.twitter_status_text)
                        post.twitter_status_id = resp.id
                        post.twitter_published = True
                        post.save()
                    if post.facebook_publish_intent:
                        facebook_api = authorized_facebook_api(post.author)
                        
                        # https://developers.facebook.com/docs/graph-api/reference/v2.2/link
                        resp = facebook_api.post(
                            path='me/feed',
                            message=post.facebook_status_text,
                            link=post.full_permalink,
                        )
                        print resp
                        post.facebook_status_id = resp["id"]
                        # print post.facebook_status_id
                        # resp = facebook_api.get(
                        #     path="/%s" % post.facebook_status_id
                        # )
                        # print resp
                        post.facebook_published = True
                        post.save()

                    print "Publish now! :)"
                    published = True
        else:
            form = SocialShareForm(instance=post)
        
        return locals()

    except:
        import traceback; traceback.print_exc();
        return HttpResponseRedirect(reverse('main_site:home'))


@login_required
@ajax_request
@csrf_exempt
def image_upload(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
        image = request.FILES['file']
        if len(image.name) > 80:
            image.name = image.name[:80]

        post_image = PostImage.objects.create(post=post, image=image)

        return {
            'success': True,
            'url': "![ImageCaption](%s)" % post_image.full_permalink,
            'blog_size_permalink': "![ImageCaption](%s)" % post_image.blog_size_permalink,
            'thumb_size_permalink': "![ImageCaption](%s)" % post_image.thumb_size_permalink,
        }
    except:
        import traceback; traceback.print_exc();
        return {
            'success': False,
        }


@ajax_request
def next_posts(request, author=None):
    if not request.user.is_authenticated():
        if "uuid" not in request.session:
            request.session["uuid"] = uuid.uuid1()
    try:
        fantastic_form = FantasticForm()
        author = Author.objects.get(slug__iexact=author)
        last_timestamp = datetime.datetime.fromtimestamp(int(request.GET["last_timestamp"]))
        posts = author.published_posts.filter(written_on__lt=last_timestamp)[:POSTS_PER_PAGINATION]
        on_blog = True
        last_timestamp = False
        if len(posts) > 0:
            last_timestamp = posts[len(posts)-1].written_on.strftime("%s")
        template = render_to_string("posts/_posts.html", RequestContext(request, locals()))
        return {
            "success": True,
            "html": template,
            "last_timestamp": last_timestamp
        }
    except:
        import traceback; traceback.print_exc();
        return {
            "success": False,
        }


@ajax_request
@login_required
def find_dayone_folder(request):
    me = request.user
    author = me.get_profile()

    client = DropboxClient(author.dropbox_access_token)
    matches = client.search("/", "Journal.dayone", file_limit=5)
    if len(matches) == 1:
        author.dropbox_dayone_folder_path = matches[0]["path"]
        author.save()
        return {"success": True}
    
    return {"success": False}

@ajax_request
@login_required
def sync_dayone(request):
    try:
        me = request.user
        author = me.get_profile()
        sync_posts.delay(author.id)
        return {"success": True}
    except:
        import traceback; traceback.print_exc();
        return {"success": False}

@ajax_request
@login_required
def sync_dayone_status(request):
    try:
        me = request.user
        author = me.get_profile()

        resp = {
            "in_sync": author.dayone_in_sync,
            "start_time": cache.get(author.sync_start_time_cache_key),
            "total": cache.get(author.sync_total_key),
            "current": cache.get(author.sync_current_key),
            "success": True
        }
        return resp
    except:
        import traceback; traceback.print_exc();
        return {"success": False}



def get_dropbox_auth_flow(web_app_session):
    redirect_uri = "%s%s" % (settings.BASE_URL, reverse("posts:dropbox_auth_finish"))
    return DropboxOAuth2Flow(settings.DROPBOX_APP_KEY, settings.DROPBOX_APP_SECRET, redirect_uri,
                             web_app_session, "dropbox-auth-csrf-token")
@login_required
def dropbox_auth_start(request):
    if "redirect_to" in request.GET:
        request.session["dropbox_auth_redirect_to"] = request.GET["redirect_to"]

    authorize_url = get_dropbox_auth_flow(request.session).start()
    return HttpResponseRedirect(authorize_url)

@login_required
def dropbox_auth_finish(request):
    try:
        access_token, user_id, url_state = \
                get_dropbox_auth_flow(request.session).finish(request.GET)
        profile = request.user.get_profile()
        profile.dropbox_access_token = access_token
        profile.dropbox_user_id = user_id
        profile.dropbox_url_state = url_state
        profile.save()

        return HttpResponseRedirect(reverse("posts:my_account"))

    except DropboxOAuth2Flow.BadRequestException, e:
        http_status(400)
    except DropboxOAuth2Flow.BadStateException, e:
        # Start the auth flow again.
        return HttpResponseRedirect(reverse("posts:dropbox_auth_start"))
    except DropboxOAuth2Flow.CsrfException, e:
        http_status(403)
    except DropboxOAuth2Flow.NotApprovedException, e:
        if "dropbox_auth_redirect_to" in request.session:
            redirect_url = request.session["dropbox_auth_redirect_to"]
            del request.session["dropbox_auth_redirect_to"]
            assert not "http:"  in redirect_url
            return HttpResponseRedirect(redirect_url)

        return HttpResponseRedirect(reverse("posts:my_account"))
    except DropboxOAuth2Flow.ProviderException, e:
        logger.log("Auth error: %s" % (e,))
        http_status(403)


# api.update_status / update_status_with_media

@login_required
def twitter_auth_start(request):
    if "redirect_to" in request.GET:
        request.session["twitter_auth_redirect_to"] = request.GET["redirect_to"]

    auth = twitter_auth()
    try:
        redirect_url = auth.get_authorization_url()
        request.session['request_token'] = (auth.request_token)
    except tweepy.TweepError:
        import traceback; traceback.print_exc();
        print 'Error! Failed to get request token.'
        return HttpResponseRedirect(reverse("posts:my_account"))

    return HttpResponseRedirect(redirect_url)

@login_required
def twitter_auth_finish(request):
    try:
        verifier = request.GET['oauth_verifier']

        auth = twitter_auth()
        token = request.session['request_token']
        del request.session['request_token']
        auth.request_token = token

        auth.get_access_token(verifier)

        author = request.user.get_profile()
        author.twitter_api_key = auth.access_token
        author.twitter_api_secret = auth.access_token_secret
        api = authorized_tweepy_api(author)

        author.twitter_full_name = api.me().name
        author.twitter_account_name = api.me().screen_name
        author.twitter_profile_picture_url = api.me().profile_image_url_https
        author.save()
    except:
        import traceback; traceback.print_exc();
        pass

    if "twitter_auth_redirect_to" in request.session:
        redirect_url = request.session["twitter_auth_redirect_to"]
        del request.session["twitter_auth_redirect_to"]
        assert not "http:"  in redirect_url
        return HttpResponseRedirect(redirect_url)
        
    return HttpResponseRedirect(reverse("posts:my_account"))


# # Get my latest posts
# graph.get('me/posts')

# # Post a photo of a parrot
# graph.post(
#     path = 'me/photos',
#     source = open('parrot.jpg', 'rb')
# )

@login_required
def facebook_auth_start(request):
    if "redirect_to" in request.GET:
        request.session["facebook_auth_redirect_to"] = request.GET["redirect_to"]

    auth = facebook_auth()
    authorization_url = auth.authorize_url('publish_actions,email,user_status')
    return HttpResponseRedirect(authorization_url)

@login_required
def facebook_auth_finish(request):
    try:
        code = request.GET["code"]
        auth = facebook_auth()
        auth.site = "https://graph.facebook.com/"
        response = auth.get_token(code)
        print response
        author = request.user.get_profile()
        author.facebook_api_key = response["access_token"][0]
        author.facebook_expire_date = datetime.datetime.now() + datetime.timedelta(seconds=int(response["expires"][0]))
        api = authorized_facebook_api(author)
        me = api.get("me")
        print me
        author.facebook_account_link = me["link"]
        author.facebook_account_name = me["name"]
        pic = api.get("me/picture?redirect=0&height=50&type=normal&width=50")
        author.facebook_profile_picture_url = pic["data"]["url"]
        author.save()
    except:
        import traceback; traceback.print_exc();
        pass
    
    if "facebook_auth_redirect_to" in request.session:
        redirect_url = request.session["facebook_auth_redirect_to"]
        del request.session["facebook_auth_redirect_to"]
        assert not "http:"  in redirect_url
        return HttpResponseRedirect(redirect_url)
    return HttpResponseRedirect(reverse("posts:my_account"))


def rss(request):
    author = get_author_from_domain(request)
    posts = Post.objects.filter(author=author, is_draft=False, email_publish_intent=True, written_on__gte=datetime.datetime.now()-datetime.timedelta(days=30)).order_by("written_on", "title")
    
    f = feedgenerator.Rss201rev2Feed(
        title=author.blog_name,
        link=author.full_blog_domain,
        description="",
        language=u"en",
        author_name=author.name,
        feed_url= "%s/rss" % author.full_blog_domain
    )
    for p in posts:
        html = ""
        if p.dayone_image_blog_size_url:
            html += "<img src='%s' style='max-width: 100%%;' />" % p.dayone_image_blog_size_url
        html += p.body_html
        # if p.description and p.description != "by %s" % p.author.name:
        #     html += "<p>%s</p>" % p.description
        # else:
        #     html += p.body_html
        title = p.title_html
        if title[:3] == "<p>" and title[-4:] == "</p>":
            title = title[3:-4]
        pubdate = None
        if p.written_on:
            pst = pytz.timezone('America/Vancouver')
            pubdate = pst.normalize(p.written_on.astimezone(pst))
        
        f.add_item(
            title=title,
            link=p.full_permalink,
            pubdate=pubdate,
            description=html,
        )
    return HttpResponse(f.writeString('UTF-8'))