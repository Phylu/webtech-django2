from django.conf.urls import patterns, url

from scorecard import views

urlpatterns = patterns('',
                       url(r'^$', views.IndexView.as_view(), name='index'),
                       url(r'^(?P<pk>\d+)/(?P<vote>-?\d)/$', views.vote, name='vote'),
                       )