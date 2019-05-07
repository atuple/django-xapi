from django.conf.urls import url, include
from .docs import *

app_name = "xapi"
urlpatterns = [
    url(r'^$', HomePageView.as_view(), name='docs_home'),
    url(r'^site/(?P<sid>\d+)/$', SitePageView.as_view(), name='docs_site'),
    url(r'^site/(?P<sid>\d+)/(?P<rid>\d+)/$', RoutePageView.as_view(), name='docs_route'),
    url(r'^site/(?P<sid>\d+)/(?P<rid>\d+)/(?P<vid>\d+)$', RoutePageView.as_view(), name='docs_view'),
]