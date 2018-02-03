from django.conf import settings
from django.conf.urls import url, include


class XApiSite(object):
    def __init__(self):
        self.routes = []

    @property
    def urls(self):
        urlpatterns = []
        # add docs view
        if settings.DEBUG:
            urlpatterns += [
                url(r'docs/', include('xapi.urls')),
            ]
        # add routes view
        for r in self.routes:
            urlpatterns += [
                url(r.path + "/" + r.version, include(r.urls))
            ]

        return urlpatterns

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
        for m in self.middleware:
            view.middleware += self.middleware
        self.registry_views += [view]

    @property
    def urls(self):
        urlpatterns = []
        for v in self.registry_views:
            urlpatterns += [url(v.path, v.as_view(), name=v.title)]
        return urlpatterns

    @property
    def register(self):
        def decorator(f):
            self.register_view(f)
            return f

        return decorator
