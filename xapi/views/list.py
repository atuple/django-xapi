from .base import ModelBaseApi
from django.views.generic.list import BaseListView
import datetime
from xapi.util import TimeFormatFactory
from django.db import models

FILTER_TAG = [
    "exact",
    "iexact",
    "contains",
    "icontains",
    "gt",
    "gte",
    "lt",
    "lte",
    "in",
    "startswith",
    "istartswith",
    "endswith",
    "iendswith",
    "range",
    "year",
    "month",
    "day",
    "isnull",
]


class ModelListApi(ModelBaseApi, BaseListView):
    method = ('GET',)
    paginate_by = 20
    count_query = 'count'
    count_only = False
    model = None
    filter_fields = "ALL"
    filter_fields_exclude = []
    display_list = []
    ordering = ["-id"]
    _model_path = "list"
    _model_title = "列表"

    def get_count_query(self):
        return self.count_query

    def get_count_only(self):
        return self.count_only

    def get(self, request, *args, **kwargs):
        if self.get_count_query() in self.request.GET:
            self.count_only = True
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        return self.get_list_context_data(**kwargs)

    def get_list_context_data(self, **kwargs):
        queryset = kwargs.pop('object_list', self.object_list)
        page_size = self.get_paginate_by(queryset)
        context = {}
        if page_size:
            paginator, page, queryset, is_paginated = self.paginate_queryset(queryset, page_size)
            self.json_layout["meta"]['pages'] = paginator.num_pages
            self.json_layout["meta"]['count'] = paginator.count
            self.json_layout["meta"]['current'] = page.number
            self.json_layout["meta"]['per_page'] = paginator.per_page
            context = self.list_serializer(queryset)
        return context

    def render_to_response(self, context):
        return self.render_response(context)

    def get_paginate_by(self, queryset):
        return self.request.GET.get("paginate_by", self.paginate_by)

    def list_serializer(self, queryset):
        return [self.model_serializer(obj) for obj in queryset]

    def get_queryset(self):
        qs = super().get_queryset()
        qs = self.get_queryset_filter(qs)
        if self.request.GET.get("order_by"):
            order_by = self.request.GET["order_by"].split(",")
            qs = qs.order_by(*order_by)
        return qs

    def get_queryset_filter(self, qs):
        filters = {}
        filter_fields = self.filter_fields if self.filter_fields != "ALL" else self._obj_fields

        for k, v in self.request.GET.items():
            if k in filter_fields and k not in self.filter_fields_exclude:
                filters[k] = self.params_value_inspect(k, v, "")
            elif "__" in k:
                f = k.split("__")[0]
                tag = k.split("__")[1]
                if tag in FILTER_TAG and f in filter_fields and f not in self.filter_fields_exclude:
                    filters[k] = self.params_value_inspect(f, v, tag)
                elif f in filter_fields and f not in self.filter_fields_exclude:
                    if isinstance(self.model._meta.get_field(f), models.ForeignKey):
                        filters[k] = self.params_value_inspect(f, v, "")
        for k, v in filters.items():
            if "lte" in k and isinstance(v, datetime.datetime):
                if v.hour == 0:
                    filters[k] = v + datetime.timedelta(minutes=59,hours=23)
        qs = qs.filter(**filters)
        return qs

    def params_value_inspect(self, field, value, tag):
        if tag == "in":
            return value.split(",")
        elif tag == "isnull" or isinstance(self.model._meta.get_field(field), models.BooleanField):
            if value == "true":
                return True
            elif value == "false":
                return False
        elif isinstance(self.model._meta.get_field(field), (models.DateField, models.DateTimeField)):
            value = TimeFormatFactory.string_to_date(value)
        return value

    def get_display(self):
        return self.display_list if self.display_list else self.display