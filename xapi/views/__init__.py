from __future__ import absolute_import
from .base import BaseApi, ModelBaseApi, BaseApiObject
from .delete import ModelDeleteApi
from .edit import PostApi, PutApi, ModelCreateApi, ModelUpdateApi
from .detail import ModelDetailApi, GetApi
from .list import ModelListApi

__all__ = (
    'BaseApiObject', 'BaseApi', 'ModelBaseApi',
    'ModelDeleteApi', 'PostApi', 'PutApi', 'ModelCreateApi', 'ModelUpdateApi',
    'ModelDetailApi', 'GetApi', 'ModelListApi'
)


def register_builtin_views(site):
    pass
