from .base import ModelBaseApi
from django.views.generic.edit import BaseDeleteView


class ModelDeleteApi(ModelBaseApi, BaseDeleteView):
    method = ('POST', 'DELETE')
    pk_url_kwarg = "id"

    def delete(self, request, *args, **kwargs):
        """
        Calls the delete() method on the fetched object and then
        redirects to the success URL.
        """
        self.object = self.get_object()
        self.object.delete()
        return self.render_response({})
