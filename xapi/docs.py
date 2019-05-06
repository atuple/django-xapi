from django.views.generic import TemplateView
from .sites import site
from markdown import markdown
from .views import ModelBaseApi, PostApi, PutApi


def _get_view_title(cls):
    if hasattr(cls, "model"):
        if cls.title:
            return cls.title
        else:
            return cls.model._meta.verbose_name.title() + "" + cls._model_title
    return cls.title


def _get_model_des(view):
    return ""


def _get_form_des(view):
    return ""


def _get_view_des(view):
    des = ""
    if issubclass(view, ModelBaseApi):
        des = _get_model_des(view)
    if issubclass(view, PostApi) or issubclass(view, PutApi):
        des = _get_form_des(view)
    return markdown(des)


class HomePageView(TemplateView):
    template_name = "xapi/home.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data()
        ctx["routes"] = site.routes
        return ctx


class RoutePageView(TemplateView):
    template_name = "xapi/route.html"

    def route_path(self, route):
        return self.request.path.split("docs")[0] + route.path + "/" + route.version

    def get_context_data(self, **kwargs):
        rid = int(kwargs["rid"])
        ctx = super().get_context_data()
        route = site.routes[rid]
        route_views = route.registry_views
        views = []
        for i in range(0, len(route_views)):
            views.append({
                "title": _get_view_title(route_views[i]),
                "path": route_views[i].path,
                "vid": i,
            })
        ctx["route"] = route
        ctx["views"] = views
        ctx["rid"] = rid
        ctx["route_path"] = self.route_path(route)

        vid = kwargs.get("vid", None)
        if vid:
            view = route_views[int(vid)]
            ctx["view"] = {
                "title": _get_view_title(view),
                "path": view.path,
                "method": view.method,
                "des": markdown(view.des) if view.des else _get_view_des(view),
                "fields": view.get_fields_des(view)
            }
        return ctx
