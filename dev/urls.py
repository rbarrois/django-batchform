# -*- coding: utf-8 -*-
# This code is distributed under the two-clause BSD license.
# Copyright (c) 2013 Raphaël Barrois


from django.urls import path

from . import views

urlpatterns = [
    path('', views.CSVUploadView.as_view(), name='example'),
]
