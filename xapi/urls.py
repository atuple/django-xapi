from django.conf.urls import url, include
from .docs import *

app_name = "xapi"
urlpatterns = [
    url(r'^$', HomePageView.as_view(), name='docs_home'),
    url(r'^route/(?P<rid>\d+)/$', RoutePageView.as_view(), name='docs_route'),
    url(r'^route/(?P<rid>\d+)/(?P<vid>\d+)/$', RoutePageView.as_view(), name='docs_view'),
]