from django.conf.urls.defaults import patterns, include, url

from main_site import views

urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),
    # url(r'^faq$', views.faq, name='faq'),
)