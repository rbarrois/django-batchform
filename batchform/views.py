# -*- coding: utf-8 -*-
# This code is distributed under the two-clause BSD license.
# Copyright (c) 2013 Raphaël Barrois


from django import forms as django_forms
from django import http
from django.contrib import messages
from django.views import generic

from . import forms


class BaseUploadView(generic.FormView):
    template_name = 'batchform/form.html'
    success_url = '/'

    STEP_UPLOAD = 'upload'
    STEP_LINES = 'lines'

    upload_form_class = None
    lines_form_class = None
    lines_formset_class = forms.LineFormSet
    columns = ()

    def __init__(self, *args, **kwargs):
        super(BaseUploadView, self).__init__(*args, **kwargs)
        self.current_step = self.STEP_UPLOAD

    # Overrides
    # =========

    def get_form(self, form_class, **extra):
        kwargs = self.get_form_kwargs()
        kwargs.update(extra)
        return form_class(**kwargs)

    def get_context_data(self, **kwargs):
        context = super(BaseUploadView, self).get_context_data(**kwargs)
        context['global_step'] = self.current_step
        return context

    # Dispatching
    # ===========

    # Control path is:
    # post() -> get_form(get_form_class()).is_valid() -> form_valid() / form_invalid()

    def post(self, request, *args, **kwargs):
        if request.POST['global_step'] not in (self.STEP_LINES, self.STEP_UPLOAD):
            raise django_forms.ValidationError(u"Invalid request.")
        self.current_step = request.POST['global_step']
        return super(BaseUploadView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        if self.current_step == self.STEP_UPLOAD:
            return self.form_upload_valid(form)
        else:
            return self.form_lines_valid(form)

    def get_form_class(self):
        if self.current_step == self.STEP_UPLOAD:
            return self.upload_form_class
        else:
            return self.lines_formset_class

    def get_form_kwargs(self):
        kwargs = super(BaseUploadView, self).get_form_kwargs()
        if self.current_step == self.STEP_LINES:
            kwargs['form'] = self.lines_form_class
        return kwargs

    # Upload
    # ======

    def form_upload_valid(self, form):
        self.current_step = self.STEP_LINES

        lines = form.cleaned_data['file']
        initial_lines = [dict(zip(self.columns, line)) for line in lines]
        lines_form = self.get_form(self.get_form_class(),
            data=None,
            files=None,
            initial=initial_lines)
        return self.render_to_response(self.get_context_data(form=lines_form))

    # Lines
    # =====

    def handle_line_form(self, line_form):
        cleaned_data = dict(line_form.cleaned_data)
        if not cleaned_data.pop('DELETE', False):
            print cleaned_data

    def form_lines_valid(self, form):
        handled = 0
        for line_form in form:
            if not line_form.cleaned_data.get('DELETE'):
                handled += 1
                self.handle_line_form(line_form)

        messages.success(self.request, u"%d lines handled" % handled)
        return http.HttpResponseRedirect(self.get_success_url())
