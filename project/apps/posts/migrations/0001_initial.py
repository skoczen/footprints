# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Author'
        db.create_table(u'posts_author', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('premium_user', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('public_domain', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('wikipedia_url', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('archive', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('archive_name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('birthdate', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('deathdate', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'posts', ['Author'])

        # Adding model 'Collection'
        db.create_table(u'posts_collection', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['posts.Author'])),
            ('title', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=800, blank=True)),
        ))
        db.send_create_signal(u'posts', ['Collection'])

        # Adding model 'Post'
        db.create_table(u'posts_post', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['posts.Author'])),
            ('title', self.gf('django.db.models.fields.TextField')(default='Title', null=True, blank=True)),
            ('body', self.gf('django.db.models.fields.TextField')(default='Body', null=True, blank=True)),
            ('is_draft', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('display_type', self.gf('django.db.models.fields.CharField')(default='poetry', max_length=50)),
            ('allow_comments', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('show_draft_revisions', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('show_published_revisions', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('longest_line', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('public_domain', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('imported', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('approximate_publication_date', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('source_url', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('audio_url', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('video_url', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('started_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('sort_datetime', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('published_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('written_on', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2014, 12, 9, 0, 0), null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=800, blank=True)),
        ))
        db.send_create_signal(u'posts', ['Post'])

        # Adding model 'PostRevision'
        db.create_table(u'posts_postrevision', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['posts.Author'])),
            ('title', self.gf('django.db.models.fields.TextField')(default='Title', null=True, blank=True)),
            ('body', self.gf('django.db.models.fields.TextField')(default='Body', null=True, blank=True)),
            ('is_draft', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('display_type', self.gf('django.db.models.fields.CharField')(default='poetry', max_length=50)),
            ('allow_comments', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('show_draft_revisions', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('show_published_revisions', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('longest_line', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('public_domain', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('imported', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('approximate_publication_date', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('source_url', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('audio_url', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('video_url', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('revised_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('post', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['posts.Post'])),
        ))
        db.send_create_signal(u'posts', ['PostRevision'])

        # Adding model 'Fantastic'
        db.create_table(u'posts_fantastic', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('post', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['posts.Post'])),
            ('uuid', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('marked_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('on', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('reader', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['posts.Author'], null=True, blank=True)),
        ))
        db.send_create_signal(u'posts', ['Fantastic'])

        # Adding model 'Read'
        db.create_table(u'posts_read', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('post', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['posts.Post'])),
            ('uuid', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('read_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('reader', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['posts.Author'], null=True, blank=True)),
        ))
        db.send_create_signal(u'posts', ['Read'])

        # Adding model 'Backup'
        db.create_table(u'posts_backup', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['posts.Author'])),
            ('zip_file', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('backup_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('num_posts', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('num_revisions', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('num_reads', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('num_fantastics', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'posts', ['Backup'])


    def backwards(self, orm):
        # Deleting model 'Author'
        db.delete_table(u'posts_author')

        # Deleting model 'Collection'
        db.delete_table(u'posts_collection')

        # Deleting model 'Post'
        db.delete_table(u'posts_post')

        # Deleting model 'PostRevision'
        db.delete_table(u'posts_postrevision')

        # Deleting model 'Fantastic'
        db.delete_table(u'posts_fantastic')

        # Deleting model 'Read'
        db.delete_table(u'posts_read')

        # Deleting model 'Backup'
        db.delete_table(u'posts_backup')


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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'premium_user': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'public_domain': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'wikipedia_url': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'posts.backup': {
            'Meta': {'ordering': "('-backup_at',)", 'object_name': 'Backup'},
            'backup_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'num_fantastics': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'num_posts': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'num_reads': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'num_revisions': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['posts.Author']"}),
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
            'approximate_publication_date': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'audio_url': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['posts.Author']"}),
            'body': ('django.db.models.fields.TextField', [], {'default': "'Body'", 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'display_type': ('django.db.models.fields.CharField', [], {'default': "'poetry'", 'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imported': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_draft': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'longest_line': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'public_domain': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'published_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'show_draft_revisions': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'show_published_revisions': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '800', 'blank': 'True'}),
            'sort_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'source_url': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'started_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.TextField', [], {'default': "'Title'", 'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'video_url': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'written_on': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2014, 12, 9, 0, 0)', 'null': 'True', 'blank': 'True'})
        },
        u'posts.postrevision': {
            'Meta': {'ordering': "('-revised_at',)", 'object_name': 'PostRevision'},
            'allow_comments': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'approximate_publication_date': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'audio_url': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['posts.Author']"}),
            'body': ('django.db.models.fields.TextField', [], {'default': "'Body'", 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'display_type': ('django.db.models.fields.CharField', [], {'default': "'poetry'", 'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imported': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_draft': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'longest_line': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['posts.Post']"}),
            'public_domain': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'revised_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'show_draft_revisions': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'show_published_revisions': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'source_url': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.TextField', [], {'default': "'Title'", 'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'video_url': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
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