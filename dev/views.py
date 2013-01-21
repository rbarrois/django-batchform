# -*- coding: utf-8 -*-

from django import forms as django_forms

from batchupload import forms, views, parsers


class CSVUploadForm(forms.BaseUploadForm):
    parsers = (parsers.CSVParser(),)


class LineForm(django_forms.Form):
    cola = django_forms.CharField(max_length=10)
    colb = django_forms.CharField(max_length=10)
    colc = django_forms.CharField(max_length=10)


class CSVUploadView(views.BaseUploadView):
    upload_form_class = CSVUploadForm
    lines_form_class = LineForm
    columns = ('cola', 'colb', 'colc')
