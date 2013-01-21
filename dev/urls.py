from django.conf.urls import patterns, include, url

from . import views

urlpatterns = patterns('',
    url(r'^$', views.CSVUploadView.as_view(), name='example'),
)
