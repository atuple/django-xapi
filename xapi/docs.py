from django.views.generic import TemplateView
from .sites import site
from markdown import markdown


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
                "title": route_views[i].title,
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
                "title": view.title,
                "path": view.path,
                "method": view.method,
                "des": markdown(view.des),
            }
        return ctx
