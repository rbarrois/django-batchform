# -*- coding: utf-8 -*-
# This code is distributed under the two-clause BSD license.
# Copyright (c) 2013 Raphaël Barrois


from django import forms as django_forms
from django import http
from django.contrib import messages
from django.forms import formsets
from django.views import generic

from . import forms


class BaseUploadView(generic.FormView):
    STEP_UPLOAD = 'upload'
    STEP_LINES = 'lines'

    # Sane defaults
    upload_template_name = 'batchform/upload_form.html'
    lines_template_name = 'batchform/lines_form.html'

    upload_form_class = forms.BaseUploadForm
    lines_formset_class = forms.LineFormSet

    # Required extensions
    inner_form_class = None
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
        if request.POST.get('global_step') not in (self.STEP_LINES, self.STEP_UPLOAD):
            raise django_forms.ValidationError(u"Invalid request.")
        self.current_step = request.POST['global_step']
        return super(BaseUploadView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        if self.current_step == self.STEP_UPLOAD:
            return self.form_upload_valid(form)
        else:
            return self.form_lines_valid(form)

    def get_lines_formset_class(self):
        """Return the class of the lines formset."""
        return self.lines_formset_class

    def get_inner_form_class(self):
        return self.inner_form_class

    def get_form_class(self):
        if self.current_step == self.STEP_UPLOAD:
            return self.upload_form_class
        else:
            lines_formset_class = self.get_lines_formset_class()
            inner_form_class = self.get_inner_form_class()
            return formsets.formset_factory(
                inner_form_class, formset=lines_formset_class,
                can_delete=lines_formset_class.can_delete)

    def get_template_names(self):
        if self.current_step == self.STEP_UPLOAD:
            return self.upload_template_name
        else:
            return self.lines_template_name

    # Upload
    # ======

    def get_columns(self):
        """Return the columns of the form."""
        return self.columns

    def form_upload_valid(self, form):
        """Handle a valid upload form."""
        self.current_step = self.STEP_LINES

        lines = form.cleaned_data['file']
        initial_lines = [dict(zip(self.get_columns(), line)) for line in lines]
        inner_form = self.get_form(self.get_form_class(),
            data=None,
            files=None,
            initial=initial_lines,
        )
        return self.render_to_response(self.get_context_data(form=inner_form))

    # Lines
    # =====

    def handle_inner_form(self, inner_form):
        """Extension point: handle valid inner forms."""
        pass

    def form_lines_valid(self, form):
        """Handle a valid LineFormSet."""
        handled = 0
        for inner_form in form:
            if not inner_form.cleaned_data.get(formsets.DELETION_FIELD_NAME):
                handled += 1
                self.handle_inner_form(inner_form)

        self.log_and_notify_lines(handled)
        return http.HttpResponseRedirect(self.get_success_url())

    def log_and_notify_lines(self, handled):
        """Called when all the lines where successfully handled."""
        messages.success(self.request, u"%d lines handled" % handled)


class FormSavingUploadView(BaseUploadView):
    """Specialized UploadView that calls form.save() on inner forms."""
    def handle_inner_form(self, inner_form):
        inner_form.save()
