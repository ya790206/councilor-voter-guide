from django.conf.urls import patterns, url
from votes import views

urlpatterns = patterns('',
    url(r'^(?P<county>)/(?P<index>normal|conscience)/$', views.select_county, name='votes'),
    url(r'^(?P<county>\S+)/(?P<index>normal|conscience)/$', views.votes, name='votes'),
    url(r'^(?P<vote_id>\S+)/$', views.vote, name='vote'),
)
