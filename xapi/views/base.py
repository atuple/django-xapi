import datetime
import decimal
from functools import update_wrapper
from django.core.serializers.json import DjangoJSONEncoder

from django.http import HttpResponse, JsonResponse, Http404
from django.utils.decorators import method_decorator, classonlymethod
from django.utils.encoding import force_text, smart_text, smart_str
from django.utils.functional import Promise
from django.utils.http import urlencode
from django.utils.safestring import mark_safe
from django.views.generic import View
from xapi.util import TimeFormatFactory, ModelFieldsFormat
import json
from django.db import models
from decimal import Decimal
from django.db.models.fields.files import ImageFieldFile, FileField


class BaseApiObject(object):
    def render_response(self, content, response_type='json'):
        self.json_layout.update({
            "code": self.http_code,
            "data": content,
            "msg": self.http_msg,
            "errors": self.http_error
        })

        return JsonResponse(self.json_layout, safe=False)

    def render_to_response(self, context):
        return self.render_response(context)

    def get_context_data(self, **kwargs):
        return {}


class BaseApi(BaseApiObject, View):
    title = ""
    des = ""
    path = ""
    auth = None
    method = ()
    model = None
    middleware = []
    datetime_format = 'string'  # 'string'  or 'timestamp'
    fields_des = {}

    def __init__(self, request, *args, **kwargs):
        if not request.method in self.method:
            raise Http404
        self.request = request
        self.request_method = request.method.lower()
        self.user = request.user
        self.time_func = TimeFormatFactory.get_time_func(self.datetime_format)
        self.args = args
        self.kwargs = kwargs

        self.http_code = 200
        self.http_error = ""
        self.http_msg = ""
        self.form_data = {}
        self.json_layout = {"meta": {}}
        self.init_request(*args, **kwargs)

    @classonlymethod
    def as_view(cls):
        def view(request, *args, **kwargs):
            for m in cls.middleware:
                result = m(request, *args, **kwargs)
                if result != True:
                    return result
            self = cls(request, *args, **kwargs)
            if hasattr(self, 'get') and not hasattr(self, 'head'):
                self.head = self.get

            if self.request_method in self.http_method_names:
                handler = getattr(
                    self, self.request_method, self.http_method_not_allowed)
            else:
                handler = self.http_method_not_allowed

            return handler(request, *args, **kwargs)

        update_wrapper(view, cls, updated=())

        return view

    def init_request(self, *args, **kwargs):
        pass

    @property
    def get_path(self):
        return self.path

    def get_fields_des(self):
        return self.fields_des


class ModelBaseApi(BaseApi):
    fields = None
    ordering = None
    model = None
    display = []
    exclude = []
    _model_path = ""
    _model_title = ""

    def __init__(self, request, *args, **kwargs):
        if not self.model:
            raise Exception('This View has not model to config')
        self._obj_fields = [f.name for f in self.model._meta.get_fields()]
        self._fields_display = self.display if self.display else self.fields_display()
        super().__init__(request, *args, **kwargs)

    def fields_display(self):
        fields_display = self.display
        if not fields_display:
            fields_display = []
            for f in self.model._meta.local_fields:
                if not hasattr(f, "local_related_fields"):
                    fields_display.append(f.name)
                else:
                    fields_display.append(f.name + "_id")
        if self.exclude:
            for f in self.exclude:
                if f in fields_display:
                    fields_display.remove(f)
        return fields_display

    def model_serializer(self, obj):
        obj_dict = {}
        for k in self._fields_display:
            value = None
            if hasattr(obj, k):
                if k in self._obj_fields or k in ["id", "pk"] or "_id" in k:
                    value = getattr(obj, k)
                else:
                    value = getattr(obj, k)()
            elif hasattr(self, k):
                value = getattr(self, k)(obj)
            elif "__" in k:
                o = obj
                for rel_k in k.split("__"):
                    o = getattr(o, rel_k)
                    value = o
            obj_dict[k] = self.field_inspect(value)

        return obj_dict

    def field_inspect(self, data):
        if isinstance(data, (datetime.datetime, datetime.date, datetime.time)):
            return self.time_func(data)
        elif isinstance(data, (ImageFieldFile, FileField)):
            return data.url if data.url else data.path
        elif isinstance(data, Decimal):
            return float(data)
        elif isinstance(data, dict):
            obj_dict = {}
            for k, v in data.items():
                obj_dict[k] = self.field_inspect(v)
            return obj_dict
        elif isinstance(data, (str, bool, float, int, list)):
            return data
        return None

    @property
    def get_path(self):
        if self.path:
            return self.path
        else:
            return self.model.__name__.lower() + "/" + self._model_path

    @property
    def get_title(self):
        if self.title:
            return self.title
        else:
            return self.model.__name__.lower() + " " + self._model_title

    def get_fields_des(self):
        fields_des = self.fields_des
        fields_des.update(ModelFieldsFormat(self.model))
        return fields_des
