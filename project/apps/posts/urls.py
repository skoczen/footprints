from django.conf.urls.defaults import patterns, include, url
import dselector
parser = dselector.Parser()
url = parser.url

from posts import views

urlpatterns = patterns('',
    # Connections
    url(r'^connect/get-dropbox-auth-flow$', views.get_dropbox_auth_flow, name='get_dropbox_auth_flow'),
    url(r'^connect/dropbox-auth-start$', views.dropbox_auth_start, name='dropbox_auth_start'),
    url(r'^connect/dropbox-auth-finish$', views.dropbox_auth_finish, name='dropbox_auth_finish'),
    url(r'^connect/find-dayone-folder$', views.find_dayone_folder, name='find_dayone_folder'),
    url(r'^connect/sync-dayone$', views.sync_dayone, name='sync_dayone'),
    url(r'^connect/sync-dayone-status$', views.sync_dayone_status, name='sync_dayone_status'),
    


    url(r'^$', views.home, name='home'),
    url(r'^explore/?$', views.explore, name='explore'),
    url(r'^my-writing/?$', views.my_writing, name='my_writing'),
    url(r'^my-reading/?$', views.my_reading, name='my_reading'),
    url(r'^my-blog/?$', views.my_blog, name='my_blog'),
    
    url(r'^my-account/?$', views.my_account, name='my_account'),
    url(r'^my-backups/?$', views.my_backups, name='my_backups'),
    url(r'^generate-backup/?$', views.generate_backup, name='generate_backup'),
    url(r'^new-post$', views.new, name='new'),
    url(r'^save/{author:slug}/{title:slug}/?$', views.save_revision, name='save_revision'),
    url(r'^fantastic/{post_id:digits}/?$', views.this_was_fantastic, name='this_was_fantastic'),
    url(r'^read/{post_id:digits}/?$', views.mark_read, name='mark_read'),
    url(r'^blog/{author:slug}/next/?$', views.next_posts, name='next_posts'),
    url(r'^blog/{author:slug}/?$', views.blog, name='blog'),

    url(r'^{author:slug}/{title:slug}/revisions/?$', views.revisions, name='revisions'),
    url(r'^{author:slug}/revision/{pk:digits}/?$', views.revision, name='revision'),
    url(r'^{author:slug}/?$', views.author, name='author'),

    # url(r'^{author:slug}/{title:slug}/revision/{revision_umb?$', views.revisions, name='revisions'),

    url(r'^{author:slug}/{title:slug}/?$', views.post, name='post'),
 

)
