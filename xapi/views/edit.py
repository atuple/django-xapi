from .base import BaseApi, ModelBaseApi
from django.views.generic.edit import BaseFormView
from django.views.generic.edit import BaseCreateView, BaseUpdateView
import json
from django import forms
from xapi.util import FormFieldsFormat


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

    def get_fields_des(self):
        fields_des = self.fields_des
        if self.form_class != forms.Form:
            fields_des.update(FormFieldsFormat(self.form_class))
        return fields_des


class PutApi(PostApi):
    def put(self, *args, **kwargs):
        return self.post(*args, **kwargs)


class ModelCreateApi(ModelBaseApi, BaseCreateView):
    method = ("POST", "PUT")
    form_class_create = None
    _model_path = "create"
    _model_title = "创建"

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

    def get_form_class(self):
        if self.form_class_create:
            self.form_class = self.form_class_create
        return super().get_form_class()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(self.get_create_context_data(**kwargs))
        return ctx

    def get_create_context_data(self, **kwargs):
        return {}


class ModelUpdateApi(ModelBaseApi, BaseUpdateView):
    method = ("POST", "PUT")
    form_class_update = None
    pk_url_kwarg = "id"
    _model_path = "update/(?P<id>\d+)"
    _model_title = "更新"

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

    def get_form_class(self):
        if self.form_class_update:
            self.form_class = self.form_class_update
        return super().get_form_class()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(self.get_update_context_data(**kwargs))
        return ctx

    def get_update_context_data(self, **kwargs):
        return {}