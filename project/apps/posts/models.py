import datetime
import re
import mistune

from django.db import models
from django.core.cache import cache
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from utils.slughifi import unique_slug, slughifi
from main_site.models import BaseModel

ENTITY_REGEX = re.compile("&[^\s]*;")
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
    facebook_account_name = models.CharField(max_length=255, blank=True, null=True)
    facebook_expire_date = models.DateTimeField(blank=True, null=True)
    twitter_api_key = models.TextField(blank=True, null=True)
    twitter_api_secret = models.TextField(blank=True, null=True)
    twitter_account_name = models.CharField(max_length=255, blank=True, null=True)
    twitter_expire_date = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.archive and not self.user:
            raise Exception("user is missing, and author is not an archive")
        self.slug = unique_slug(self, 'name', 'slug')
        super(Author, self).save(*args, **kwargs)

    @property
    def published_posts(self):
        return self.post_set.filter(is_draft=False).order_by("-written_on").all()

    @property
    def dayone_sync_cache_key(self):
        return "DayOne-In-Sync-%s" % self.pk

    @property
    def dayone_in_sync(self):
        return cache.get(self.dayone_sync_cache_key) == True

    @property
    def dayone_sync_start_time_cache_key(self):
        return "DayOne-In-Sync-Started-%s" % self.pk

    @property
    def dayone_sync_total_key(self):
        return "DayOne-In-Sync-Total-%s" % self.pk

    @property
    def dayone_sync_current_key(self):
        return "DayOne-In-Sync-Current-%s" % self.pk

    def start_dayone_sync(self):
        cache.set(self.dayone_sync_cache_key, True)

    def finish_dayone_sync(self):
        cache.delete(self.dayone_sync_cache_key, True)

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
        return False

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
    post_type = models.IntegerField(choices=POST_TYPES)
    num_images = models.IntegerField(default=0)

    is_draft = models.BooleanField(default=True)
    allow_comments = models.BooleanField(default=True)

    dayone_post = models.BooleanField(default=False, editable=False)
    dayone_id = models.CharField(max_length=255, blank=True, null=True, editable=False)
    dayone_posted = models.DateTimeField(blank=True, null=True, editable=False)
    dayone_last_modified = models.DateTimeField(blank=True, null=True, editable=False)
    dayone_last_rev = models.CharField(max_length=255, blank=True, null=True, editable=False)
    dayone_image = models.ImageField(upload_to="dayone_images", blank=True, null=True)

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

    twitter_published = models.BooleanField(default=False, editable=False)
    twitter_status_text = models.TextField(blank=True, null=True)
    twitter_status_id = models.CharField(max_length=255, blank=True, null=True, editable=False)


    def __unicode__(self, *args, **kwargs):
        return self.title

    def save(self, *args, **kwargs):
        self.title_html = mistune.markdown(self.title)
        self.body_html = mistune.markdown(self.body)

        self.num_images = self.body_html.count("<img")
        if self.dayone_image:
            self.num_images += 1

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

class Post(AbstractPost):
    started_at = models.DateTimeField(blank=True, null=True, editable=False, auto_now_add=True)
    sort_datetime = models.DateTimeField(blank=True, null=True, editable=False)
    published_at = models.DateTimeField(blank=True, null=True, editable=False)
    written_on = models.DateTimeField(blank=True, null=True, default=datetime.datetime.now())
    slug = models.CharField(max_length=800, blank=True, verbose_name="url")

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

        # if make_revision:
        #     cleaned_body = self.body.replace("<br/>", "\n").replace("<br>", "\n").replace("</div>", "\n")
        #     cleaned_body = ENTITY_REGEX.sub(" ", cleaned_body)
            
        self.sort_datetime = self.date
        super(Post, self).save(*args, **kwargs)

        if make_revision and self.title != "Title" and self.body != "Body":
            INVALID_FIELDS = ["written_on", "started_at", "sort_datetime", "published_at", "id", "pk", "slug"]
            post_dict = {}
            for k, v in self.__dict__.items():
                if k not in INVALID_FIELDS and k[0] != "_":
                    post_dict[k] = v
            post_dict["post"] = self
            PostRevision.objects.create(**post_dict)

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


# def create_user_profile(sender, instance, created, **kwargs):
#     print sender
#     print kwargs
#     if created and not Author.objects.filter(user=instance).count() > 0:
        
#         Author.objects.create(user=instance)

# post_save.connect(create_user_profile, sender=User, dispatch_uid="create_user_profile")
