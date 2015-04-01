from django.conf.urls import patterns, url

from scorecard import views

urlpatterns = patterns('',
                       url(r'^$', views.IndexView.as_view(), name='index'),
                       url(r'^vote/(?P<pk>\d+)/(?P<vote>-?\d)/$', views.vote, name='vote'),
                       url(r'^details/(?P<pk>\d+)$', views.details, name='details'),
                       url(r'^vote_again$', views.vote_again, name='vote_again'),
                       url(r'^statistics', views.statistics, name="statistics"),
                       )