from .base import ModelBaseApi
from django.views.generic.edit import BaseDeleteView


class ModelDeleteApi(ModelBaseApi, BaseDeleteView):
    method = ('POST', 'DELETE')
    pk_url_kwarg = "id"
    _model_path = "delete/(?P<id>\d+)"
    _model_title = "删除"

    def delete(self, request, *args, **kwargs):
        """
        Calls the delete() method on the fetched object and then
        redirects to the success URL.
        """
        if request.GET.get("ids"):
            ids = request.GET["ids"]
            if ids == "all":
                self.model.objects.all().delete()
            elif "," in ids:
                ids = ids.split(",")
                self.model.objects.filter(id__in=ids).delete()
        else:
            self.object = self.get_object()
            self.object.delete()
        return self.render_response({})
