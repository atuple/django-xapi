from django.conf import settings
from django.conf.urls import url, include
from django.urls import path
from .views import ModelListApi, ModelCreateApi, ModelDeleteApi, ModelUpdateApi, ModelDetailApi


def _get_view_path(cls):
    if hasattr(cls, "model"):
        if cls.path:
            return cls.path
        else:
            return cls.model.__name__.lower() + "/" + cls._model_path
    return cls.path


class XApiSite(object):
    def __init__(self):
        self.routes = []

    @property
    def urls(self):
        urlpatterns = []
        # add docs view
        if settings.DEBUG:
            urlpatterns += [
                url(r'docs/', ('xapi.urls', 'xapi', 'xapi')),
            ]
        # add routes view
        for r in self.routes:
            urlpatterns += [
                url(r.path + "/" + r.version, r.urls)
            ]

        return urlpatterns, "xapi", "xapi"

    def register(self, route):
        self.routes += [route]


site = XApiSite()


class Router(object):
    def __init__(self, path, title="xapi", des="", verison="v1"):
        self.path = path
        self.title = title
        self.des = des
        self.version = verison
        self.registry_views = []
        self.middleware = []
        site.register(self)

    # 注册视图
    def register_view(self, view):
        if not hasattr(view, "middleware"):
            view.middleware = []
        view.middleware = self.middleware + view.middleware
        self.registry_views += [view]

    @property
    def urls(self):
        urlpatterns = []
        for v in self.registry_views:
            urlpatterns += [url(_get_view_path(v), v.as_view(), name=v.title)]
        return urlpatterns, 'route', "route"

    @property
    def register(self):
        def decorator(f):
            self.register_view(f)
            return f

        return decorator

    def _register_model(self, models, admin_class):
        model_path = admin_class if hasattr(admin_class, "model_path") else models.__name__.lower()
        for cls_view in [ModelListApi, ModelDetailApi, ModelCreateApi, ModelDeleteApi, ModelUpdateApi]:
            admin_class.model = models
            new_cls = type(models.__name__ + cls_view.__name__, (admin_class, cls_view), dict())
            new_cls.path = _get_view_path(new_cls)
            self.register_view(new_cls)

    def register_model(self, models, **kwargs):

        def _model_admin_wrapper(admin_class):
            self._register_model(models, admin_class)

        return _model_admin_wrapper
