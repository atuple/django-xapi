from .base import BaseApi, ModelBaseApi
from django.views.generic.edit import BaseFormView

from django.views.generic.edit import BaseCreateView, BaseUpdateView
import json
from django import forms


class PostApi(BaseApi, BaseFormView):
    form_class = forms.Form
    method = ('POST', 'PUT')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if 'application/json' in self.request.content_type:
            kwargs.update({
                'data': json.loads(self.request.body),
            })
        return kwargs

    def form_valid(self, form):
        self.form_data = form.data
        return self.render_response(self.get_context_data())

    def form_invalid(self, form):
        context = self.get_context_data()
        self.http_code = 401
        self.http_error = form.errors
        return self.render_response(context)


class PutApi(PostApi):
    def put(self, *args, **kwargs):
        return self.post(*args, **kwargs)


class ModelCreateApi(ModelBaseApi, BaseCreateView):
    method = ("POST", "PUT")

    def init_request(self, *args, **kwargs):
        super().init_request()
        if not self.fields:
            self.fields = [field.name for field in iter(self.model._meta.local_fields) if field.editable]

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if 'application/json' in self.request.content_type:
            kwargs.update({
                'data': json.loads(self.request.body),
            })
        return kwargs

    def form_valid(self, form):
        self.form_data = form.data
        return self.render_response(self.get_context_data())

    def form_invalid(self, form):
        context = self.get_context_data()
        self.http_code = 401
        self.http_error = form.errors
        return self.render_response(context)


class ModelUpdateApi(ModelBaseApi, BaseUpdateView):
    method = ("POST", "PUT")
    pk_url_kwarg = "id"

    def init_request(self, *args, **kwargs):
        super().init_request()
        if not self.fields:
            self.fields = [field.name for field in iter(self.model._meta.local_fields) if field.editable]

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if 'application/json' in self.request.content_type:
            kwargs.update({
                'data': json.loads(self.request.body),
            })
        return kwargs

    def form_valid(self, form):
        self.form_data = form.data
        form.save()
        return self.render_response(self.get_context_data())

    def form_invalid(self, form):
        context = self.get_context_data()
        self.http_code = 401
        self.http_error = form.errors
        return self.render_response(context)
