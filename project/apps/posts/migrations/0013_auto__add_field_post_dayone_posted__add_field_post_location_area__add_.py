# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Post.dayone_posted'
        db.add_column(u'posts_post', 'dayone_posted',
                      self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Post.location_area'
        db.add_column(u'posts_post', 'location_area',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Post.location_country'
        db.add_column(u'posts_post', 'location_country',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Post.latitude'
        db.add_column(u'posts_post', 'latitude',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Post.longitude'
        db.add_column(u'posts_post', 'longitude',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Post.location_name'
        db.add_column(u'posts_post', 'location_name',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Post.time_zone_string'
        db.add_column(u'posts_post', 'time_zone_string',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Post.weather_temp_f'
        db.add_column(u'posts_post', 'weather_temp_f',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Post.weather_temp_c'
        db.add_column(u'posts_post', 'weather_temp_c',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Post.weather_description'
        db.add_column(u'posts_post', 'weather_description',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Post.weather_icon'
        db.add_column(u'posts_post', 'weather_icon',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Post.weather_pressure'
        db.add_column(u'posts_post', 'weather_pressure',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Post.weather_relative_humidity'
        db.add_column(u'posts_post', 'weather_relative_humidity',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Post.weather_wind_bearing'
        db.add_column(u'posts_post', 'weather_wind_bearing',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Post.weather_wind_chill_c'
        db.add_column(u'posts_post', 'weather_wind_chill_c',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Post.weather_wind_speed_kph'
        db.add_column(u'posts_post', 'weather_wind_speed_kph',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'PostRevision.dayone_posted'
        db.add_column(u'posts_postrevision', 'dayone_posted',
                      self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'PostRevision.location_area'
        db.add_column(u'posts_postrevision', 'location_area',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'PostRevision.location_country'
        db.add_column(u'posts_postrevision', 'location_country',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'PostRevision.latitude'
        db.add_column(u'posts_postrevision', 'latitude',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'PostRevision.longitude'
        db.add_column(u'posts_postrevision', 'longitude',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'PostRevision.location_name'
        db.add_column(u'posts_postrevision', 'location_name',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'PostRevision.time_zone_string'
        db.add_column(u'posts_postrevision', 'time_zone_string',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'PostRevision.weather_temp_f'
        db.add_column(u'posts_postrevision', 'weather_temp_f',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'PostRevision.weather_temp_c'
        db.add_column(u'posts_postrevision', 'weather_temp_c',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'PostRevision.weather_description'
        db.add_column(u'posts_postrevision', 'weather_description',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'PostRevision.weather_icon'
        db.add_column(u'posts_postrevision', 'weather_icon',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'PostRevision.weather_pressure'
        db.add_column(u'posts_postrevision', 'weather_pressure',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'PostRevision.weather_relative_humidity'
        db.add_column(u'posts_postrevision', 'weather_relative_humidity',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'PostRevision.weather_wind_bearing'
        db.add_column(u'posts_postrevision', 'weather_wind_bearing',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'PostRevision.weather_wind_chill_c'
        db.add_column(u'posts_postrevision', 'weather_wind_chill_c',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'PostRevision.weather_wind_speed_kph'
        db.add_column(u'posts_postrevision', 'weather_wind_speed_kph',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Post.dayone_posted'
        db.delete_column(u'posts_post', 'dayone_posted')

        # Deleting field 'Post.location_area'
        db.delete_column(u'posts_post', 'location_area')

        # Deleting field 'Post.location_country'
        db.delete_column(u'posts_post', 'location_country')

        # Deleting field 'Post.latitude'
        db.delete_column(u'posts_post', 'latitude')

        # Deleting field 'Post.longitude'
        db.delete_column(u'posts_post', 'longitude')

        # Deleting field 'Post.location_name'
        db.delete_column(u'posts_post', 'location_name')

        # Deleting field 'Post.time_zone_string'
        db.delete_column(u'posts_post', 'time_zone_string')

        # Deleting field 'Post.weather_temp_f'
        db.delete_column(u'posts_post', 'weather_temp_f')

        # Deleting field 'Post.weather_temp_c'
        db.delete_column(u'posts_post', 'weather_temp_c')

        # Deleting field 'Post.weather_description'
        db.delete_column(u'posts_post', 'weather_description')

        # Deleting field 'Post.weather_icon'
        db.delete_column(u'posts_post', 'weather_icon')

        # Deleting field 'Post.weather_pressure'
        db.delete_column(u'posts_post', 'weather_pressure')

        # Deleting field 'Post.weather_relative_humidity'
        db.delete_column(u'posts_post', 'weather_relative_humidity')

        # Deleting field 'Post.weather_wind_bearing'
        db.delete_column(u'posts_post', 'weather_wind_bearing')

        # Deleting field 'Post.weather_wind_chill_c'
        db.delete_column(u'posts_post', 'weather_wind_chill_c')

        # Deleting field 'Post.weather_wind_speed_kph'
        db.delete_column(u'posts_post', 'weather_wind_speed_kph')

        # Deleting field 'PostRevision.dayone_posted'
        db.delete_column(u'posts_postrevision', 'dayone_posted')

        # Deleting field 'PostRevision.location_area'
        db.delete_column(u'posts_postrevision', 'location_area')

        # Deleting field 'PostRevision.location_country'
        db.delete_column(u'posts_postrevision', 'location_country')

        # Deleting field 'PostRevision.latitude'
        db.delete_column(u'posts_postrevision', 'latitude')

        # Deleting field 'PostRevision.longitude'
        db.delete_column(u'posts_postrevision', 'longitude')

        # Deleting field 'PostRevision.location_name'
        db.delete_column(u'posts_postrevision', 'location_name')

        # Deleting field 'PostRevision.time_zone_string'
        db.delete_column(u'posts_postrevision', 'time_zone_string')

        # Deleting field 'PostRevision.weather_temp_f'
        db.delete_column(u'posts_postrevision', 'weather_temp_f')

        # Deleting field 'PostRevision.weather_temp_c'
        db.delete_column(u'posts_postrevision', 'weather_temp_c')

        # Deleting field 'PostRevision.weather_description'
        db.delete_column(u'posts_postrevision', 'weather_description')

        # Deleting field 'PostRevision.weather_icon'
        db.delete_column(u'posts_postrevision', 'weather_icon')

        # Deleting field 'PostRevision.weather_pressure'
        db.delete_column(u'posts_postrevision', 'weather_pressure')

        # Deleting field 'PostRevision.weather_relative_humidity'
        db.delete_column(u'posts_postrevision', 'weather_relative_humidity')

        # Deleting field 'PostRevision.weather_wind_bearing'
        db.delete_column(u'posts_postrevision', 'weather_wind_bearing')

        # Deleting field 'PostRevision.weather_wind_chill_c'
        db.delete_column(u'posts_postrevision', 'weather_wind_chill_c')

        # Deleting field 'PostRevision.weather_wind_speed_kph'
        db.delete_column(u'posts_postrevision', 'weather_wind_speed_kph')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '255'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'posts.author': {
            'Meta': {'object_name': 'Author'},
            'archive': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'archive_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'birthdate': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'deathdate': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'dropbox_access_token': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'dropbox_dayone_entry_hash': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'dropbox_dayone_folder_path': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'dropbox_dayone_image_hash': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'dropbox_expire_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'dropbox_url_state': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'dropbox_user_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'facebook_account_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'facebook_api_key': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'facebook_expire_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_dropbox_sync': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'premium_user': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'public_domain': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'twitter_account_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'twitter_api_key': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'twitter_expire_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'wikipedia_url': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'posts.backup': {
            'Meta': {'ordering': "('-backup_at',)", 'object_name': 'Backup'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['posts.Author']"}),
            'backup_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'num_fantastics': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'num_posts': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'num_reads': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'num_revisions': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'zip_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'posts.collection': {
            'Meta': {'object_name': 'Collection'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['posts.Author']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '800', 'blank': 'True'}),
            'title': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'posts.fantastic': {
            'Meta': {'object_name': 'Fantastic'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'marked_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'on': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['posts.Post']"}),
            'reader': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['posts.Author']", 'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'})
        },
        u'posts.post': {
            'Meta': {'ordering': "('-started_at',)", 'object_name': 'Post'},
            'allow_comments': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['posts.Author']"}),
            'body': ('django.db.models.fields.TextField', [], {'default': "'Body'", 'null': 'True', 'blank': 'True'}),
            'body_html': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dayone_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'dayone_last_modified': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'dayone_last_rev': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'dayone_post': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'dayone_posted': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_draft': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'location_area': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'location_country': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'location_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'published_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '800', 'blank': 'True'}),
            'sort_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'started_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'time_zone_string': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.TextField', [], {'default': "'Title'", 'null': 'True', 'blank': 'True'}),
            'title_html': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'weather_description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'weather_icon': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'weather_pressure': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'weather_relative_humidity': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'weather_temp_c': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'weather_temp_f': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'weather_wind_bearing': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'weather_wind_chill_c': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'weather_wind_speed_kph': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'written_on': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2014, 12, 12, 0, 0)', 'null': 'True', 'blank': 'True'})
        },
        u'posts.postrevision': {
            'Meta': {'ordering': "('-revised_at',)", 'object_name': 'PostRevision'},
            'allow_comments': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['posts.Author']"}),
            'body': ('django.db.models.fields.TextField', [], {'default': "'Body'", 'null': 'True', 'blank': 'True'}),
            'body_html': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dayone_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'dayone_last_modified': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'dayone_last_rev': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'dayone_post': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'dayone_posted': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_draft': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'location_area': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'location_country': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'location_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['posts.Post']"}),
            'revised_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'time_zone_string': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.TextField', [], {'default': "'Title'", 'null': 'True', 'blank': 'True'}),
            'title_html': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'weather_description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'weather_icon': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'weather_pressure': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'weather_relative_humidity': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'weather_temp_c': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'weather_temp_f': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'weather_wind_bearing': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'weather_wind_chill_c': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'weather_wind_speed_kph': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'posts.read': {
            'Meta': {'object_name': 'Read'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['posts.Post']"}),
            'read_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'reader': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['posts.Author']", 'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['posts']