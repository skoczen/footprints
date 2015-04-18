import datetime
import math
import re
import markdown
from pyembed.markdown import PyEmbedMarkdown

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.cache import cache
# from django.core.cache.utils import make_template_fragment_key
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save
from sorl.thumbnail import get_thumbnail
from utils.slughifi import unique_slug, slughifi
from main_site.models import BaseModel
from .util import FencedCodeExtension

ENTITY_REGEX = re.compile("&[^\s]*;")
BODY_HTML_CACHE_KEY = "post_body_%(pk)s"
TITLE_HTML_CACHE_KEY = "post_title_%(pk)s"
BIG_QUOTE = 1
PHOTO_WITH_CAPTION = 2
ARTICLE_SINGLE_IMAGE = 3
ARTICLE_MULTIPLE_IMAGES = 4
BODY_WITH_NO_TITLE = 5
POST_TYPES = [
    (BIG_QUOTE, "Big Quote"),
    (PHOTO_WITH_CAPTION, "Photo with caption"),
    (ARTICLE_SINGLE_IMAGE, "Article and a Single Image"),
    (ARTICLE_MULTIPLE_IMAGES, "Article and a multiple images"),
    (BODY_WITH_NO_TITLE, "Body with no real title"),
]


class Author(BaseModel):
    user = models.ForeignKey("auth.User", blank=True, null=True)
    premium_user = models.BooleanField(default=False)
    slug = models.CharField(max_length=255, blank=True, editable=False)
    blog_name = models.CharField(max_length=255, blank=True)
    blog_domain = models.CharField(max_length=255, blank=True, null=True, unique=True)
    blog_header = models.TextField(blank=True, null=True)
    blog_footer = models.TextField(blank=True, null=True)

    public_domain = models.BooleanField(default=False)
    wikipedia_url = models.TextField(blank=True, null=True)
    archive = models.BooleanField(default=False)
    archive_name = models.CharField(max_length=255, blank=True, editable=False)
    birthdate = models.DateField(blank=True, null=True)
    deathdate = models.DateField(blank=True, null=True)
    dropbox_access_token = models.CharField(max_length=255, blank=True, null=True)
    dropbox_user_id = models.CharField(max_length=255, blank=True, null=True)
    dropbox_url_state = models.CharField(max_length=255, blank=True, null=True)
    dropbox_expire_date = models.DateTimeField(blank=True, null=True)
    dropbox_dayone_folder_path = models.CharField(max_length=255, blank=True, null=True)
    dropbox_dayone_entry_hash = models.CharField(max_length=255, blank=True, null=True)
    dropbox_dayone_image_hash = models.CharField(max_length=255, blank=True, null=True)
    last_dropbox_sync =  models.DateTimeField(blank=True, null=True)
    facebook_api_key = models.TextField(blank=True, null=True)
    facebook_account_link = models.TextField(blank=True, null=True)
    facebook_account_name = models.CharField(max_length=255, blank=True, null=True)
    facebook_expire_date = models.DateTimeField(blank=True, null=True)
    facebook_profile_picture_url = models.TextField(blank=True, null=True)
    twitter_api_key = models.TextField(blank=True, null=True)
    twitter_api_secret = models.TextField(blank=True, null=True)
    twitter_full_name = models.CharField(max_length=255, blank=True, null=True)
    twitter_account_name = models.CharField(max_length=255, blank=True, null=True)
    twitter_expire_date = models.DateTimeField(blank=True, null=True)
    twitter_profile_picture_url = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.archive and not self.user:
            raise Exception("user is missing, and author is not an archive")
        self.slug = unique_slug(self, 'name', 'slug')
        super(Author, self).save(*args, **kwargs)

    @property
    def published_posts(self):
        return self.post_set.filter(is_draft=False).order_by("-written_on").all()

    @property
    def sync_cache_key(self):
        return "DayOne-In-Sync-%s" % self.pk

    @property
    def dayone_in_sync(self):
        return cache.get(self.sync_cache_key) == True

    @property
    def sync_start_time_cache_key(self):
        return "DayOne-In-Sync-Started-%s" % self.pk

    @property
    def sync_total_key(self):
        return "DayOne-In-Sync-Total-%s" % self.pk

    @property
    def sync_current_key(self):
        return "DayOne-In-Sync-Current-%s" % self.pk

    def start_dayone_sync(self):
        cache.set(self.sync_cache_key, True)

    def finish_dayone_sync(self):
        cache.delete(self.sync_cache_key, True)

    @property
    def name(self):
        if self.archive and self.archive_name:
            return self.archive_name
        return self.user.first_name

    @property
    def name_ends_in_s(self):
        return self.name[-1] == "s"

    @property
    def most_recent_update(self):
        if self.post_set.order_by("-sort_datetime").count() > 0:
            return self.post_set.order_by("-sort_datetime")[0].sort_datetime
        else:
            return None

    @property
    def start_date(self):
        return self.created_at

    @property
    def dropbox_valid(self):
        return self.dropbox_access_token and self.dropbox_user_id

    @property
    def dayone_valid(self):
        return self.dropbox_valid and self.dropbox_dayone_folder_path

    @property
    def num_dayone_posts(self):
        return self.post_set.filter(dayone_post=True).count()

    @property
    def twitter_valid(self):
        return self.twitter_api_secret and self.twitter_api_key and self.twitter_account_name
    
    @property
    def facebook_valid(self):
        return self.facebook_api_key and self.facebook_account_name

    @property
    def full_blog_domain(self):
        return "http://%s" % self.blog_domain

    @property
    def redirects(self):
        return self.redirect_set.order_by("old_url").all()
    
    def __unicode__(self):
        return "%s" % self.name


class Collection(BaseModel):
    author = models.ForeignKey(Author)
    title = models.TextField(blank=True, null=True)
    slug = models.CharField(max_length=800, blank=True, editable=False)

    def save(self, *args, **kwargs):
        self.slug = unique_slug(self, 'title', 'slug')
        super(Collection, self).save(*args, **kwargs)

    def __unicode__(self):
        return "%s" % self.title


class AbstractPost(BaseModel):
    author = models.ForeignKey(Author)
    title = models.TextField(blank=True, null=True, default="Title")
    body = models.TextField(blank=True, null=True, default="Body")
    title_html = models.TextField(blank=True, null=True, editable=False)
    body_html = models.TextField(blank=True, null=True, editable=False)
    description = models.TextField(blank=True, null=True)
    post_type = models.IntegerField(choices=POST_TYPES)
    num_images = models.IntegerField(default=0)
    permalink_path = models.CharField(max_length=500, blank=True, null=True, editable=False)
    num_read_seconds = models.IntegerField(default=60)
    num_read_minutes = models.IntegerField(default=60)

    is_draft = models.BooleanField(default=True)
    prospect = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    allow_comments = models.BooleanField(default=True)

    dayone_post = models.BooleanField(default=False, editable=False)
    dayone_posted = models.DateTimeField(blank=True, null=True, editable=False)
    dayone_last_modified = models.DateTimeField(blank=True, null=True, editable=False)
    dayone_last_rev = models.CharField(max_length=255, blank=True, null=True, editable=False)
    dayone_image = models.ImageField(verbose_name="Hero Image", upload_to="dayone_images", blank=True, null=True)
    dayone_image_url = models.TextField(blank=True, null=True)
    dayone_image_blog_size_url = models.TextField(blank=True, null=True)
    dayone_image_thumb_size_url = models.TextField(blank=True, null=True)
    dayone_image_related_size_url = models.TextField(blank=True, null=True)

    location_area = models.CharField(max_length=255, blank=True, null=True,)
    location_country = models.CharField(max_length=255, blank=True, null=True,)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    location_name = models.CharField(max_length=255, blank=True, null=True, editable=False)
    time_zone_string = models.CharField(max_length=255, blank=True, null=True, editable=False)

    weather_temp_f = models.IntegerField(blank=True, null=True)
    weather_temp_c = models.IntegerField(blank=True, null=True)
    weather_description = models.CharField(max_length=255, blank=True, null=True, editable=False)
    weather_icon = models.CharField(max_length=255, blank=True, null=True, editable=False)
    weather_pressure = models.IntegerField(blank=True, null=True)
    weather_relative_humidity = models.IntegerField(blank=True, null=True)
    weather_wind_bearing = models.IntegerField(blank=True, null=True)
    weather_wind_chill_c = models.IntegerField(blank=True, null=True)
    weather_wind_speed_kph = models.IntegerField(blank=True, null=True)

    twitter_publish_intent = models.BooleanField(default=True)
    twitter_include_image = models.BooleanField(default=True)
    twitter_published = models.BooleanField(default=False, editable=False)
    twitter_status_text = models.TextField(blank=True, null=True)
    twitter_status_id = models.CharField(max_length=255, blank=True, null=True, editable=False)
    twitter_retweets = models.IntegerField(blank=True, null=True, default=0)
    twitter_favorites = models.IntegerField(blank=True, null=True, default=0)
    twitter_mentions = models.IntegerField(blank=True, null=True, default=0)

    facebook_publish_intent = models.BooleanField(default=True)
    facebook_published = models.BooleanField(default=False, editable=False)
    facebook_status_text = models.TextField(blank=True, null=True)
    facebook_status_id = models.CharField(max_length=255, blank=True, null=True, editable=False)
    facebook_likes = models.IntegerField(blank=True, null=True, default=0)
    facebook_shares = models.IntegerField(blank=True, null=True, default=0)
    facebook_comments = models.IntegerField(blank=True, null=True, default=0)

    social_shares_customized = models.BooleanField(default=False)

    email_publish_intent = models.BooleanField(default=False)
    allow_private_viewing = models.BooleanField(default=False)
    custom_pitch = models.TextField(blank=True, null=True)

    def __unicode__(self, *args, **kwargs):
        return self.title

    def save(self, *args, **kwargs):
        self.title_html = markdown.markdown(self.title, extensions=[
            FencedCodeExtension(),
            # 'markdown.extensions.extra',
            PyEmbedMarkdown(),
            # 'markdown.extensions.codehilite',
            # 'fenced-code-blocks',
            # 'cuddled-lists',
            # 'footnotes',
            # 'smarty-pants',
        ]).replace("http://www.youtube.com", "https://www.youtube.com")
        if self.title_html[:3] == "<p>" and self.title_html[-4:] == "</p>":
            self.title_html = self.title_html[3:-4]
        self.body_html = markdown.markdown(self.body, extensions=[
            FencedCodeExtension(),
            # 'markdown.extensions.extra',
            PyEmbedMarkdown(),
            # 'markdown.extensions.codehilite',
            # 'fenced-code-blocks',
            # 'cuddled-lists',
            # 'footnotes',
            # 'smarty-pants',
        ]).replace("http://www.youtube.com", "https://www.youtube.com")

        self.num_images = self.body_html.count("<img")
        if not self.description or self.description == "Body" or self.description == "by %s" % self.author.name:
            if self.body and self.body != "Body":
                self.description = self.body[:160]
            else:
                self.description = "by %s" % self.author.name
        if self.dayone_image:
            self.num_images += 1

        # lines = self.body.count("<br/>") + self.body.count("<br>") + self.body.count("<p/>")
        chars = len(self.body)
        # Average reading speed of 300 wpm, 5 letters per word plus a space.
        self.num_read_seconds = round(1.0 * chars / 6 / 250 * 60)
        self.num_read_minutes = round(self.num_read_seconds / 60.0)

        # Invalidate any cached template.
        # cache.delete(make_template_fragment_key('blog_post', [self.pk]))

        super(AbstractPost, self).save(*args, **kwargs)

    class Meta:
        abstract = True



    @property
    def is_big_quote(self):
        return self.post_type == BIG_QUOTE

    @property
    def is_photo_with_caption(self):
        return self.post_type == PHOTO_WITH_CAPTION

    @property
    def is_article_single_image(self):
        return self.post_type == ARTICLE_SINGLE_IMAGE

    @property
    def is_article_multiple_images(self):
        return self.post_type == ARTICLE_MULTIPLE_IMAGES

    @property
    def is_body_with_no_title(self):
        return self.post_type == BODY_WITH_NO_TITLE

    @property
    def twitter_url(self):
        return "https://twitter.com/%s/status/%s" % (self.author.twitter_account_name, self.twitter_status_id)

    @property
    def facebook_url(self):
        sections = self.facebook_status_id.split("_")
        return "%sposts/%s" % (self.author.facebook_account_link, sections[1])

    @property
    def all_published(self):
        return self.facebook_published and self.twitter_published

    @property
    def email_published(self):
        return self.email_publish_intent

    @property
    def num_facebook_activity(self):
        return (self.facebook_likes or 0) + (self.facebook_shares or 0) + (self.facebook_comments or 0)

    @property
    def num_twitter_activity(self):
        return (self.twitter_favorites or 0) + (self.twitter_retweets or 0) + (self.twitter_mentions or 0)

    @property
    def permalink(self):
        if self.permalink_path:
            return self.permalink_path
        else:
            return reverse('posts:post', args=(self.slug,))

    def get_absolute_url(self):
        return self.full_permalink

    @property
    def full_permalink(self):
        return "%s%s" % (self.author.full_blog_domain, self.permalink)

    @property
    def pitch(self):
        if self.custom_pitch:
            return self.custom_pitch
        else:
            return "Find my writing valuable?  Please consider <a href='https://www.patreon.com/inkandfeet' target='_blank'>supporting me</a> on Patreon."


class Post(AbstractPost):
    started_at = models.DateTimeField(blank=True, null=True, editable=False, auto_now_add=True)
    sort_datetime = models.DateTimeField(blank=True, null=True, editable=False)
    published_at = models.DateTimeField(blank=True, null=True, editable=False)
    written_on = models.DateTimeField(blank=True, null=True, default=datetime.datetime.now())
    slug = models.CharField(max_length=800, blank=True, verbose_name="url")

    dayone_id = models.CharField(max_length=255, blank=True, null=True, editable=False, unique=True)

    def save(self, *args, **kwargs):
        if not self.published_at and not self.is_draft:
            self.published_at = datetime.datetime.now()

        # Post type.
        if self.num_images == 0 and not self.body:
            self.post_type = BIG_QUOTE
        elif self.num_images == 1 and not self.body:
            self.post_type = PHOTO_WITH_CAPTION
        elif self.num_images == 1:
            self.post_type = ARTICLE_SINGLE_IMAGE
        elif self.body and len(self.title) > 120:
            self.post_type = BODY_WITH_NO_TITLE
        else:
            self.post_type = ARTICLE_MULTIPLE_IMAGES



        make_revision = False
        update_thumbs = False
        if not self.pk:
            make_revision = True
            if not self.title:
                self.slug = "%s" % self.dayone_id.split(".")[0]
            else:
                self.slug = unique_slug(self, 'title', 'slug', generate_new=True)
        else:
            old_me = Post.objects.get(pk=self.pk)
            if slughifi(old_me.title) != slughifi(self.title):
                if not self.title:
                    self.slug = "%s" % self.dayone_id.split(".")[0]
                else:
                    self.slug = unique_slug(self, 'title', 'slug', generate_new=True)

            if old_me.title != self.title or old_me.body != self.body:
                make_revision = True

            if not self.is_draft:
                if not self.permalink_path or old_me.is_draft:
                    self.permalink_path = reverse('posts:post', args=(self.slug,))
            if old_me.dayone_image != self.dayone_image:
                self.dayone_image_url = self.dayone_image.url.split("?")[0]
                update_thumbs = True

        if not self.social_shares_customized:
            self.twitter_status_text = "%s %s" % (self.title.strip()[:118], self.full_permalink)

            if self.title and self.body:
                self.facebook_status_text = "%s\n\n%s" % (self.title.strip(), self.body.strip(),)
            elif self.body:
                self.facebook_status_text = self.body.strip()
            else:
                self.facebook_status_text = self.title.strip()

            if len(self.facebook_status_text) > 450:
                self.facebook_status_text = "%s...\nRead the rest at: %s" % (self.facebook_status_text[:410], self.full_permalink)
        # if make_revision:
        #     cleaned_body = self.body.replace("<br/>", "\n").replace("<br>", "\n").replace("</div>", "\n")
        #     cleaned_body = ENTITY_REGEX.sub(" ", cleaned_body)

        self.sort_datetime = self.date
        super(Post, self).save(*args, **kwargs)

        if make_revision and self.title != "Title" and self.body != "Body":
            INVALID_FIELDS = ["written_on", "started_at", "sort_datetime", "published_at", "id", "pk", "slug", "dayone_id"]
            post_dict = {}
            for k, v in self.__dict__.items():
                if k not in INVALID_FIELDS and k[0] != "_":
                    post_dict[k] = v
            post_dict["post"] = self
            PostRevision.objects.create(**post_dict)

        if update_thumbs:
            self.dayone_image_thumb_size_url = get_thumbnail(self.dayone_image, '100x100', crop="center", quality=75).url.split("?")[0]
            self.dayone_image_blog_size_url = get_thumbnail(self.dayone_image, '1792', quality=90).url.split("?")[0]
            self.dayone_image_related_size_url = get_thumbnail(self.dayone_image, '504x384', crop="center", quality=85).url.split("?")[0]
            self.save()

    @property
    def date(self):
        if not self.is_draft:
            return self.published_at
        else:
            if self.has_been_revised:
                return self.most_recent_revision.revised_at
            else:
                return self.started_at

    @property
    def most_recent_revision(self):
        return self.postrevision_set.all().order_by("-revised_at")[0]

    @property
    def has_been_revised(self):
        return self.postrevision_set.all().count() > 1

    @property
    def revisions(self):
        return self.postrevision_set.all()

    @property
    def revisions_visible(self):
        return (
                (self.is_draft and self.show_draft_revisions) or
                (not self.is_draft and self.show_published_revisions)
               ) and self.has_been_revised

    @property
    def num_fantastics(self):
        return self.fantastic_set.filter(on=True).count()

    @property
    def num_reads(self):
        return self.read_set.all().count()

    @property
    def all_images(self):
        return self.postimage_set.all()

    def __unicode__(self):
        return "%s" % self.title

    class Meta:
        ordering = ("-started_at",)


class PostRevision(AbstractPost):
    revised_at = models.DateTimeField(auto_now_add=True, editable=False)
    post = models.ForeignKey(Post)

    class Meta:
        ordering = ("-revised_at",)

    def __unicode__(self):
        return "%s (%s)" % (self.title, self.revised_at)


class PostImage(BaseModel):
    post = models.ForeignKey(Post)
    image = models.ImageField(upload_to="post_images", blank=True, null=True)
    image_url = models.TextField(blank=True, null=True)
    blog_size_url = models.TextField(blank=True, null=True)
    thumb_size_url = models.TextField(blank=True, null=True)

    @property
    def full_permalink(self):
        return self.image_url

    @property
    def blog_size_permalink(self):
        return self.blog_size_url

    @property
    def thumb_size_permalink(self):
        return self.thumb_size_url

    def save(self, *args, **kwargs):
        resave = False
        if self.pk:
            old_me = PostImage.objects.get(pk=self.pk)
            if old_me.image != self.image:
                resave = True
        else:
            resave = True

        super(PostImage, self).save(*args, **kwargs)
        
        if resave:
            self.image_url = self.image.url.split("?")[0]
            self.thumb_size_url = get_thumbnail(self.image, '100x100', crop="center", quality=75).url.split("?")[0]
            self.blog_size_url = get_thumbnail(self.image, '1792', quality=90).url.split("?")[0]
            self.save()

class Fantastic(BaseModel):
    post = models.ForeignKey(Post)
    uuid = models.CharField(max_length=500, blank=True, null=True)
    marked_at = models.DateTimeField(auto_now_add=True, editable=False)
    on = models.BooleanField(default=True)

    reader = models.ForeignKey(Author, blank=True, null=True)


class Read(BaseModel):
    post = models.ForeignKey(Post)
    uuid = models.CharField(max_length=500, blank=True, null=True)
    read_at = models.DateTimeField(auto_now_add=True, editable=False)

    reader = models.ForeignKey(Author, blank=True, null=True)

    @property
    def fantasticed_this_post(self):
        return Fantastic.objects.filter(reader=self.reader, post=self.post, on=True)

    # class Meta:
    #     ordering = ("-read_at",)

class Backup(BaseModel):
    author = models.ForeignKey(Author)
    zip_file = models.FileField(upload_to="backups", blank=True, null=True)
    backup_at = models.DateTimeField(blank=True, null=True, editable=False, auto_now_add=True)
    num_posts = models.IntegerField(default=0)
    num_revisions = models.IntegerField(default=0)
    num_reads = models.IntegerField(default=0)
    num_fantastics = models.IntegerField(default=0)

    class Meta:
        ordering = ("-backup_at",)

class Redirect(BaseModel):
    author = models.ForeignKey(Author)
    old_url = models.CharField(max_length=600, blank=True, null=True)
    new_url = models.CharField(max_length=600, blank=True, null=True)


# def create_user_profile(sender, instance, created, **kwargs):
#     print sender
#     print kwargs
#     if created and not Author.objects.filter(user=instance).count() > 0:
        
#         Author.objects.create(user=instance)

# post_save.connect(create_user_profile, sender=User, dispatch_uid="create_user_profile")
