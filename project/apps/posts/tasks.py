import codecs
import datetime
import hashlib
import os
import plistlib
import shutil
from StringIO import StringIO
import tempfile
import time
import zipfile

from celery.task import task, periodic_task
from dropbox.client import DropboxClient
from django.core.cache import cache
from django.core.files.base import ContentFile

MAX_SYNC_TIMEOUT = datetime.timedelta(minutes=5)

# Sometimes, it's just faster not to reinvent the wheel.
# Via http://stackoverflow.com/questions/1855095/how-to-create-a-zip-archive-of-a-directory-in-python
def make_zipfile(output_filename, source_dir):
    relroot = os.path.abspath(os.path.join(source_dir, os.pardir))
    with zipfile.ZipFile(output_filename, "w", zipfile.ZIP_DEFLATED) as zip:
        for root, dirs, files in os.walk(source_dir):
            # add directory (needed for empty dirs)
            zip.write(root, os.path.relpath(root, relroot))
            for file in files:
                filename = os.path.join(root, file)
                if os.path.isfile(filename): # regular files only
                    arcname = os.path.join(os.path.relpath(root, relroot), file)
                    zip.write(filename, arcname)



@task
def generate_backup_zip(author_id):
    from django.core.files import File
    from posts.models import Author, Backup

    try:
        author = Author.objects.get(pk=author_id)
    except:
        print "Could not find author %s" % author_id
        return

    temp_folder_path = tempfile.mkdtemp()
    backup_folder_path = os.path.join(temp_folder_path, "Backup")
    os.mkdir(backup_folder_path)
    now = datetime.datetime.now()

    # backup structure
    # /Author-Name-footprints-backup-2014-05-16.zip
    #     /Posts
    #        Post-Title.html
    #     /Revisions
    #        /Post-Title.html
    #           Post-Title-2014-03-21-12.56.12pm.html
    #     Read-List.html
    #     Fantastic-List.html

    post_folder = os.path.join(backup_folder_path, "Posts")
    os.mkdir(post_folder)
    for p in author.post_set.all():
        with codecs.open(os.path.join(post_folder, "%s.html" % p.slug), "w+", "utf-8") as f:
            f.write("<h1>%s</h1>\n" % p.title)
            f.write(p.body.replace("<br/>", "<br/>\n"))

    revisions_folder = os.path.join(backup_folder_path, "Revisions")
    os.mkdir(revisions_folder)
    for p in author.postrevision_set.all():
        revision_folder = os.path.join(revisions_folder, p.post.slug[:100])

        if not os.path.exists(revision_folder):
            os.mkdir(revision_folder)

        revision_filename = os.path.join(
            revision_folder,
            "%s-%s.html" % (p.post.slug[:100], p.revised_at.strftime("%Y-%m-%d.%H.%M.%s"))
        )
        counter = 1
        while os.path.exists(revision_filename):
            revision_filename = os.path.join(
                revision_folder,
                "%s-%s-%s.html" % (p.post.slug[:100], p.revised_at.strftime("%Y-%m-%d.%H.%M.%s"), counter)
            )
            counter += 1

        with codecs.open(revision_filename, "w+", "utf-8") as f:
            f.write("Revised %s\n\n" % p.revised_at.strftime("%c"))
            f.write("<h1>%s</h1>\n" % p.title)
            f.write(p.body.replace("<br/>", "<br/>\n"))

    # Read List
    with open(os.path.join(backup_folder_path, "read-list.html"), "w+") as f:
        f.write("<h1>Read list</h1>\n")
        for r in author.read_set.all():
            f.write("On %s: %s by %s<br/>\n" % (r.read_at.strftime("%Y-%m-%d"), r.post.title, r.post.author.name))

    # Fantastic-List
    with open(os.path.join(backup_folder_path, "fantastic-list.html"), "w+") as f:
        f.write("<h1>Fantastic list:</h1>\n")
        for r in author.fantastic_set.all():
            f.write("On %s: %s by %s<br/>\n" % (r.marked_at.strftime("%Y-%m-%d"), r.post.title, r.post.author.name))

    # Footprints.txt
    with open(os.path.join(backup_folder_path, "footprints.txt"), "w+") as f:
        f.write("This backup file was generated by footprints.org on %s." % (now.strftime("%B %d, %Y"),))

    # Write the file
    zip_name = os.path.join(temp_folder_path, '%s-footprints-backup-%s.zip' % (
        author.name, now.strftime("%Y-%m-%d")
    ))
    make_zipfile(zip_name, backup_folder_path)

    b = Backup.objects.create(
        author=author,
        num_posts=author.post_set.all().count(),
        num_revisions=author.postrevision_set.all().count(),
        num_reads=author.read_set.all().count(),
        num_fantastics=author.fantastic_set.all().count(),
    )
    with open(zip_name, 'r') as f:
        b.zip_file = File(f)
        b.save()

    shutil.rmtree(temp_folder_path)


@periodic_task(run_every=datetime.timedelta(seconds=120))
def periodic_sync():
    from posts.models import Author
    for a in Author.objects.all():
        print "%s: %s" % (a, a.dayone_valid)
        print cache.get(a.sync_start_time_cache_key)
        sync_posts(a.pk)


def get_from_plist_if_exists(key, plist):
    try:
        node = plist
        for segment in key.split("."):
            node = node[segment]
        return node
    except:
        return None

def get_matching_image_meta_if_exists(dayone_id, image_list):
    for i in image_list["contents"]:
        if i["path"].split("/")[-1].split(".")[0] == dayone_id.split(".")[0]:
            return i
    return None

def datetime_from_utc_to_local(utc_datetime):
    now_timestamp = time.time()
    offset = datetime.datetime.fromtimestamp(now_timestamp) - datetime.datetime.utcfromtimestamp(now_timestamp)
    return utc_datetime + datetime.timedelta(hours=7)

@task
def sync_posts(author_id):
    from posts.models import Author, Post
    from posts.social import twitter_auth, authorized_tweepy_api, facebook_auth, authorized_facebook_api
    author = Author.objects.get(pk=author_id)
    if cache.get(author.sync_cache_key) is None or cache.get(author.sync_start_time_cache_key) is None or cache.get(author.sync_start_time_cache_key)+MAX_SYNC_TIMEOUT < datetime.datetime.now():
        try:
            cache.set(author.sync_cache_key, True)
            cache.set(author.sync_start_time_cache_key, datetime.datetime.now())
            cache.set(author.sync_total_key, "~%s" % cache.get(author.sync_total_key, "0"))
            cache.set(author.sync_current_key, 0)

            if author.dayone_valid:
                client = DropboxClient(author.dropbox_access_token)
                full_dayone_entry_path = "%s/entries" % author.dropbox_dayone_folder_path
                full_dayone_image_path = "%s/photos" % author.dropbox_dayone_folder_path
                file_list = client.metadata(full_dayone_entry_path)
                image_list = client.metadata(full_dayone_image_path)

                cache.set(author.sync_total_key, len(file_list["contents"]))
                count = 0
                for f in file_list["contents"]:
                    do_update = False
                    dayone_id = f["path"].split("/")[-1]

                    cache.set(author.sync_current_key, count)
                    exists = False
                    if Post.objects.filter(dayone_id=dayone_id).count() > 0:
                        exists = True
                        p = Post.objects.get(dayone_id=dayone_id)
                        if p.dayone_last_rev != f["revision"]:
                            dayone_update_time = datetime_from_utc_to_local(datetime.datetime(*time.strptime(f["modified"], '%a, %d %b %Y %H:%M:%S +0000')[:6]))
                            if dayone_update_time > p.updated_at:
                                do_update = True
                            if not do_update:
                                image = get_matching_image_meta_if_exists(dayone_id, image_list)
                                if image:
                                    image_update_time = datetime_from_utc_to_local(datetime.datetime(*time.strptime(image["modified"], '%a, %d %b %Y %H:%M:%S +0000')[:6]))
                                    if image_update_time > p.updated_at:
                                        do_update = True
                    else:
                        do_update = True

                    if do_update:
                        if not cache.get(author.sync_cache_key):
                            print "Interrupted."
                            break;

                        with client.get_file(f["path"]) as fh:
                            plist = plistlib.readPlist(fh)
                        content = u"%s" % plist["Entry Text"]

                        split = content.split("\n")
                        title = split[0]

                        body = "\n".join(split[1:])
                        draft = "Publish URL" not in plist
                        
                        image = get_matching_image_meta_if_exists(dayone_id, image_list)
                        if image:
                            print "getting image"
                            m = hashlib.sha1()
                            m.update("%s %s" % (dayone_id, datetime.datetime.now()))
                            image_name = "%s%s" % (dayone_id.split(".")[0], m.hexdigest())

                        kwargs = {
                            "author": author,
                            "title": title,
                            "body": body,
                            "dayone_post": True,
                            "dayone_id": dayone_id,
                            
                            "dayone_last_modified": datetime_from_utc_to_local(datetime.datetime(*time.strptime(f["modified"], '%a, %d %b %Y %H:%M:%S +0000')[:6])),
                            "dayone_last_rev": f["revision"],
                            "is_draft": draft,
                            "dayone_posted": datetime_from_utc_to_local(get_from_plist_if_exists("Creation Date", plist)),
                            "written_on": get_from_plist_if_exists("Creation Date", plist),
                            
                            "location_area": get_from_plist_if_exists("Location.Administrative Area", plist),
                            "location_country": get_from_plist_if_exists("Location.Country", plist),
                            "latitude": get_from_plist_if_exists("Location.Latitude", plist),
                            "longitude": get_from_plist_if_exists("Location.Longitude", plist),
                            "location_name": get_from_plist_if_exists("Location.Place Name", plist),
                            "time_zone_string": get_from_plist_if_exists("Location.Time Zone", plist),
                            
                            "weather_temp_f": get_from_plist_if_exists("Weather.Fahrenheit", plist),
                            "weather_temp_c": get_from_plist_if_exists("Weather.Celsius", plist),
                            "weather_description": get_from_plist_if_exists("Weather.Description", plist),
                            "weather_icon": get_from_plist_if_exists("Weather.IconName", plist),
                            "weather_pressure": get_from_plist_if_exists("Weather.Pressure MB", plist),
                            "weather_relative_humidity": get_from_plist_if_exists("Weather.Relative Humidity", plist),
                            "weather_wind_bearing": get_from_plist_if_exists("Weather.Wind Bearing", plist),
                            "weather_wind_chill_c": get_from_plist_if_exists("Weather.Wind Chill Celsius", plist),
                            "weather_wind_speed_kph": get_from_plist_if_exists("Weather.Wind Speed KPH", plist),
                        }
                        if exists:
                            if not p.is_draft:
                                kwargs["is_draft"] = False

                            for (key, value) in kwargs.items():
                                setattr(p, key, value)
                            if image:
                                image_file = client.get_file(image["path"])
                                p.dayone_image.save(
                                    "%s.jpg" % image_name,
                                    ContentFile(StringIO(image_file.read()).getvalue())
                                )
                                image_file.close()
                            p.save()
                        else:
                            p = Post.objects.create(**kwargs)
                            if image:
                                image_file = client.get_file(image["path"])

                                p.dayone_image.save(
                                    "%s.jpg" % image_name,
                                    ContentFile(StringIO(image_file.read()).getvalue())
                                )

                                p.save()
                                image_file.close()
                        

                        print p.slug
                    count += 1

                author.last_dropbox_sync = datetime.datetime.now()
                author.save()

            # Pull all social stats:
            twitter_api = authorized_tweepy_api(author)
            facebook_api =  authorized_facebook_api(author)
            for p in author.published_posts:
                # Twitter
                do_save = False
                if p.twitter_published:
                    try:
                        status = twitter_api.get_status(p.twitter_status_id)
                        p.twitter_retweets = status.retweet_count
                        p.twitter_favorites = status.favorite_count
                        do_save = True
                    except:
                        p.twitter_published = False
                        p.twitter_status_id = None
                        p.twitter_retweets = 0
                        p.twitter_favorites = 0
                        do_save = True
                        import traceback; traceback.print_exc();
                        pass

                # Facebook
                if p.facebook_published:
                    try:
                        try:
                            print p.facebook_status_id
                            resp = facebook_api.get(
                                path="/%s" % p.facebook_status_id
                            )
                            resp = facebook_api.get(
                                path="/%s/likes/?summary=true" % p.facebook_status_id
                            )
                            print resp
                            if "summary" in resp:
                                p.facebook_likes = resp["summary"]["total_count"]

                            resp = facebook_api.get(
                                path="/%s/comments/?summary=true" % p.facebook_status_id
                            )
                            print resp
                            if "summary" in resp:
                                p.facebook_comments = resp["summary"]["total_count"]

                            resp = facebook_api.get(
                                path="/%s/sharedposts/?summary=true" % p.facebook_status_id
                            )
                            print resp
                            if "summary" in resp:
                                p.facebook_shares = resp["summary"]["total_count"]

                            try:
                                resp = facebook_api.get(
                                    path="/%s" % p.full_permalink
                                )
                                print resp
                                if "share" in resp:
                                    if not p.facebook_shares:
                                        p.facebook_shares = 0
                                    p.facebook_shares = p.facebook_shares + resp["share"]["share_count"]
                                print p.facebook_shares
                            except:
                                import traceback; traceback.print_exc();

                            do_save = True
                        except:
                            import traceback; traceback.print_exc();
                            pass
                        # p.facebook_published = False
                        # p.facebook_status_id = None
                        # p.facebook_likes = 0
                        # p.facebook_shares = 0
                        # p.facebook_comments = 0
                    except:
                        # p.facebook_published = False
                        # p.facebook_status_id = None
                        # p.facebook_likes = 0
                        # p.facebook_shares = 0
                        # p.facebook_comments = 0
                        # do_save = True
                        pass

                        
                        pass
                if do_save:
                    p.save()

        except:
            import traceback; traceback.print_exc();
            pass
        cache.delete(author.sync_cache_key)
        cache.delete(author.sync_start_time_cache_key)
    else:
        print "Sync for %s already running." % author
    print "Done"