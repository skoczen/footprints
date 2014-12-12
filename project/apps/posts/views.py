import uuid

from dropbox.client import DropboxOAuth2Flow, DropboxClient

from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import Http404
from django.db.models import Count
from django.db.models import Max, Min
from django.views.decorators.csrf import csrf_exempt
from annoying.decorators import render_to, ajax_request
from posts.models import Backup, Fantastic, Post, Author, PostRevision, Read
from posts.forms import AccountForm, FantasticForm, PostForm, ReadForm
from posts.tasks import generate_backup_zip

@render_to("posts/home.html")
def home(request):
    return locals()


def my_writing(request):
    try:
        author = request.user.get_profile()
        return HttpResponseRedirect(reverse("posts:author", args=(author.slug,)))
    except:
        return HttpResponseRedirect("%s?next=%s" % (reverse("account_login",), reverse("posts:my_writing")))


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


@render_to("posts/author.html")
def author(request, author=None):
    author = Author.objects.get(slug__iexact=author)
    if author.user == request.user:
        is_me = True
        posts = Post.objects.filter(author=author).order_by("-written_on", "title")
    else:
        is_me = False
        posts = Post.objects.filter(author=author, is_draft=False).order_by("-written_on", "title")
    return locals()


@render_to("posts/post.html")
def post(request, author=None, title=None):
    if not request.user.is_authenticated():
        if "uuid" not in request.session:
            request.session["uuid"] = uuid.uuid1()
    post = Post.objects.get(slug__iexact=title, author__slug__iexact=author)
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
    new_url = None
    post = Post.objects.get(slug__iexact=title, author__slug__iexact=author)
    old_slug = post.slug
    was_published = not post.is_draft
    is_mine = post.author.user == request.user
    if not is_mine:
        raise Exception("Either this isn't your post, or you're not logged in!")

    success = False
    form = PostForm(request.POST, instance=post)
    if form.is_valid():
        new_post = form.save()
        success = True
        if old_slug != new_post.slug or not was_published and not new_post.is_draft:
            new_url = reverse("posts:post", args=(post.author.slug, new_post.slug,))
    else:
        print form

    return {"success": success, "new_url": new_url}


@render_to("posts/revisions.html")
def revisions(request, author=None, title=None):
    post = Post.objects.get(slug__iexact=title, author__slug__iexact=author)
    is_mine = post.author.user == request.user
    if is_mine:
        revisions = post.revisions
    elif post.show_draft_revisions:
        if (post.show_published_revisions):
            revisions = post.revisions
        else:
            revisions = post.revisions.filter(is_draft=True)
    else:
        if post.show_published_revisions:
            revisions = post.revisions.filter(is_draft=False)
        else:
            revisions = post.revisions.none()

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
        return HttpResponseRedirect(reverse("posts:post", args=(post.author.slug, post.post.slug) ))

    return locals()


def new(request):
    author = Author.objects.get(user=request.user)
    post = Post.objects.create(author=author)
    return HttpResponseRedirect("%s?editing=true" % reverse("posts:post", args=(post.author.slug, post.slug,)))


@ajax_request
def this_was_fantastic(request, post_id):
    post = Post.objects.get(pk=post_id)

    fantastic_form = FantasticForm(request.POST)
    if fantastic_form.is_valid():
        fantastic = fantastic_form.save(commit=False)
        fantastic.post = post
        if request.user.is_authenticated():
            fantastic.reader = request.user.get_profile()
        else:
            if "uuid" in request.session:
                fantastic.uuid = request.session["uuid"]
            fantastic.reader = None
        fantastic.save()

        return {"success": True, "num_people": post.num_fantastics}

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




@ajax_request
@login_required
def find_dayone_folder(request):
    me = request.user
    author = me.get_profile()

    client = DropboxClient(author.dropbox_access_token)
    matches = client.search("/", "Journal.dayone", file_limit=5)
    if len(matches) == 1:
        author.dropbox_day_one_folder_path = matches[0]["path"]
        author.save()
        return {"success": True}
    
    return {"success": False}

def get_dropbox_auth_flow(web_app_session):
    redirect_uri = "%s%s" % (settings.BASE_URL, reverse("posts:dropbox_auth_finish"))
    return DropboxOAuth2Flow(settings.DROPBOX_APP_KEY, settings.DROPBOX_APP_SECRET, redirect_uri,
                             web_app_session, "dropbox-auth-csrf-token")

def dropbox_auth_start(request):
    authorize_url = get_dropbox_auth_flow(request.session).start()
    return HttpResponseRedirect(authorize_url)

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
        flash('Not approved?  Why not?')
        return HttpResponseRedirect(reverse("posts:my_account"))
    except DropboxOAuth2Flow.ProviderException, e:
        logger.log("Auth error: %s" % (e,))
        http_status(403)