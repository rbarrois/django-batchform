# -*- coding: utf-8 -*-
# This code is distributed under the two-clause BSD license.
# Copyright (c) 2013 Raphaël Barrois

from django import forms

from batchform import views


class LineForm(forms.Form):
    cola = forms.CharField(max_length=10)
    colb = forms.CharField(max_length=10)
    colc = forms.CharField(max_length=10, required=True)


class CSVUploadView(views.BaseUploadView):
    inner_form_class = LineForm
    columns = ('cola', 'colb', 'colc')
    success_url = '/'
