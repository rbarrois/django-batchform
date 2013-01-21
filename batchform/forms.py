# -*- coding: utf-8 -*-


from django import forms
from django.forms import formsets

from . import parsers as parsers_mod


class BaseUploadForm(forms.Form):
    file = forms.FileField()

    parsers = ()

    def get_parsers(self):
        return self.parsers

    def clean_file(self):
        """Analyse the uploaded file, and return the parsed lines.

        Returns:
            tuple of tuples of cells content (as text).
        """
        data = self.cleaned_data['file']

        parsers = self.get_parsers()

        for parser in parsers:
            try:
                return parser.parse_file(data)
            except parsers_mod.ParserError:
                pass

        raise forms.ValidationError(
            u"No parser could read the file. Tried with parsers %s." %
            (u", " % (unicode(p) for p in parsers)))


class LineFormSet(formsets.BaseFormSet):
    form = None
    can_order = False
    can_delete = True
    extra = 0
    max_num = 0

    unique_fields = ()

    def __init__(self, *args, **kwargs):
        self.form = kwargs.pop('form', None) or self.form
        if 'initial' in kwargs:
            self.max_num = len(kwargs['initial'])
        super(LineFormSet, self).__init__(*args, **kwargs)

    def clean(self):
        """Global cleanup."""
        super(LineFormSet, self).clean()

        if any(self.errors):
            # Already seen errors, let's skip.
            return

        self.clean_unique_fields()

    def clean_unique_fields(self):
        """Ensure 'unique fields' are unique among entered data."""
        if not self.unique_fields:
            return

        keys = set()
        duplicates = []

        for form in self.forms:
            key = tuple(form.cleaned_data[field] for field in self.unique_fields)
            if key in keys:
                duplicates.append(u",".join(key))
            else:
                keys.add(key)

        if duplicates:
            raise forms.ValidationError(
                u"Fields %s should be unique; found duplicates for %s" % (
                    u','.join(self.unique_fields), duplicates))
