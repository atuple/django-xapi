import time
import datetime
from django.db import models
from django.forms import ChoiceField

try:
    from django.utils import timezone
except ImportError:
    raise RuntimeError('Django is required for Django Xapi.')


class TimeFormatFactory(object):
    def __init__(self):
        super(TimeFormatFactory, self).__init__()

    @staticmethod
    def datetime_to_string(datetime_time, time_format='%Y-%m-%d %H:%M'):  # %Y-%m-%d %H:%M:%S
        if isinstance(datetime_time, datetime.datetime):
            if datetime_time.tzinfo:
                datetime_time = datetime_time.astimezone(timezone.get_current_timezone())
            return datetime_time.strftime(time_format)
        elif isinstance(datetime_time, datetime.time):
            time_format = '%H:%M:%S'
        elif isinstance(datetime_time, datetime.date):
            time_format = '%Y-%m-%d'
        return datetime_time.strftime(time_format)

    @staticmethod
    def datetime_to_timestamp(datetime_time, time_format=None):
        if isinstance(datetime_time, datetime.datetime):
            if datetime_time.tzinfo:
                datetime_time = datetime_time.astimezone(timezone.get_current_timezone())
            return time.mktime(datetime_time.timetuple())
        return time.mktime(datetime_time.timetuple())

    @staticmethod
    def get_time_func(func_type='string'):
        if func_type == 'string':
            return TimeFormatFactory.datetime_to_string
        elif func_type == 'timestamp':
            return TimeFormatFactory.datetime_to_timestamp
        else:
            return TimeFormatFactory.datetime_to_string

    @staticmethod
    def string_to_date(string_date):
        return datetime.datetime.strptime(string_date, '%Y-%m-%d')


def ModelFieldsFormat(model):
    data = {}
    for f in model._meta.local_fields:
        f_name = f.name if not hasattr(f, "local_related_fields") else f.name + "_id"
        f_type = str(f.__class__).split(".")[-1].split("Field")[0].split("'")[0]
        f_verbose_name = f.verbose_name
        f_default = "" if "NOT_PROVIDED" in str(f.default) else f.default
        f_help_text = f.help_text
        f_choices = ""
        f_null = False if f.null else True

        if f.choices:
            for i in f.choices:
                f_choices += "%s == %s </br>" % (i[1], i[0])

        if f_name != "None":
            data[f_name] = {
                "name": f_name,
                "type": f_type,
                "verbose_name": f_verbose_name,
                "default": f_default,
                "help_text": f_help_text,
                "choices": f_choices,
                "null": f_null
            }
    return data


def FormFieldsFormat(form):
    data = {}
    for name, field in form.base_fields.items():
        choices = ""
        if isinstance(field.widget, ChoiceField):
            for i in field.widget.choices:
                choices += "%s == %s </br>" % (i[1], i[0])
        data[name] = {
            "name": name,
            "type": str(field.__class__).split(".")[-1].split("Field")[0].split("'")[0],
            "verbose_name": field.label or name,
            "default": field.initial or "",
            "help_text": field.help_text,
            "choices": choices,
            "null": field.required
        }
    return data
