django-batchform
================

This project aims to provide a simple yet powerful way to fill
a batch of forms from a single uploaded file (CSV, xlsx, ...).

It uses Django class-based generic views to that effect, allowing for a very simple configuration:

.. code-block:: python

    from django import forms
    from batchform import views

    class LineForm(forms.Form):
        col1 = forms.CharField(max_length=10)
        col2 = forms.CharField(max_length=10)
        col3 = forms.CharField(max_length=10)

    class BatchFormView(views.BaseUploadView):
        lines_form_class = LineForm
        columns = ('col1', 'col2', 'col3')

Demo
====

In order to have a look at the application, simply clone the repository,
ensure you have Django in your repository, and run::

  ./manage.py runserver


Links
=====

- Package on PyPI: http://pypi.python.org/pypi/django-batchform/
- Source code on Github: https://github.com/rbarrois/django-batchform/
- Doc on ReadTheDocs: (TODO)
- Continuous integration on Travis-CI (TODO)
