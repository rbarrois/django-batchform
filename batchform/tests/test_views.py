# -*- coding: utf-8 -*-
# This code is distributed under the two-clause BSD license.
# Copyright (c) 2013 Raphaël Barrois

from __future__ import unicode_literals

import os.path


from django import forms
from django.test import TestCase
import django.contrib.messages.storage.cookie as cookie_storage


data_dir = os.path.join(os.path.dirname(__file__), 'data')


def decode_cookie_messages(cookie):
    """Decode a cookie encoded by CookieStorage
    """
    return cookie_storage.CookieStorage(request=None)._decode(cookie)


class BaseTestCase(TestCase):
    urls = 'dev.urls'

    def open_data(self, filename, *args, **kwargs):
        absolute_path = os.path.join(data_dir, filename)
        return open(absolute_path, *args, **kwargs)


class UploadTestCase(BaseTestCase):

    def test_upload_form(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'batchform/upload_form.html')

    def test_uploaded_file(self):
        with self.open_data('example.csv', 'rb') as f:
            response = self.client.post('/', {'file': f, 'global_step': 'upload'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'batchform/lines_form.html')
        self.assertContains(response, "foo")
        self.assertContains(response, "bar")

    def test_missing_global_step(self):
        with self.open_data('example.csv', 'rb') as f:
            self.assertRaises(forms.ValidationError, self.client.post,
                '/', {'file': f})


class LinesTestCase(BaseTestCase):
    def test_lines_form(self):
        response = self.client.post('/', {
            'global_step': 'lines',
            'form-TOTAL_FORMS': '3',
            'form-INITIAL_FORMS': '3',
            'form-MAX_NUM_FORMS': '3',
            'form-0-cola': '1',
            'form-0-colb': '2',
            'form-0-colc': '3',
            'form-1-cola': 'foo',
            'form-1-colb': 'bar',
            'form-1-colc': 'baz',
            'form-2-cola': 'blih',
            'form-2-colb': 'blah',
            'form-2-colc': 'bleh',
        })

        self.assertRedirects(response, '/')
        self.assertIn("3 lines", decode_cookie_messages(response.cookies['messages'].value)[0].message)

    def test_incomplete_form(self):
        response = self.client.post('/', {
            'global_step': 'lines',
            'form-TOTAL_FORMS': '3',
            'form-INITIAL_FORMS': '3',
            'form-MAX_NUM_FORMS': '3',
            'form-0-cola': '1',
            'form-0-colb': '2',
            'form-0-colc': '3',
            'form-1-cola': 'foo',
            'form-1-colb': 'bar',
            'form-1-colc': 'baz',
            'form-2-cola': 'blih',
            'form-2-colb': '',  # Missing required field
            'form-2-colc': 'bleh',
        })

        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'batchform/lines_form.html')
        self.assertContains(response, 'foo')
        self.assertContains(response, 'bar')
        self.assertContains(response, 'blih')
        self.assertContains(response, "required")

    def test_lines_form_with_deleted(self):
        response = self.client.post('/', {
            'global_step': 'lines',
            'form-TOTAL_FORMS': '3',
            'form-INITIAL_FORMS': '3',
            'form-MAX_NUM_FORMS': '3',
            'form-0-cola': '1',
            'form-0-colb': '2',
            'form-0-colc': '3',
            'form-1-cola': 'foo',
            'form-1-colb': 'bar',
            'form-1-colc': 'baz',
            'form-1-DELETE': 'on',
            'form-2-cola': 'blih',
            'form-2-colb': 'blah',
            'form-2-colc': 'bleh',
        })

        self.assertRedirects(response, '/')
        self.assertIn("2 lines", decode_cookie_messages(response.cookies['messages'].value)[0].message)
