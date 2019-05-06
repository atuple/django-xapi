from .base import BaseApi, ModelBaseApi
from django.views.generic.detail import BaseDetailView

class GetApi(BaseApi):
    method = ('GET',)

    def get_context_data(self):
        return {}

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        response = self.render_response(context)
        return response


class ModelDetailApi(ModelBaseApi, BaseDetailView):
    model = None
    method = ('GET',)
    pk_url_kwarg = "id"
    _model_path = "detail/(?P<id>\d+)"
    _model_title = "详情"

    def get_context_data(self, **kwargs):
        context = {}
        if self.object:
            context = self.model_serializer(self.object)
        return context