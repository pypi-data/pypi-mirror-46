from django.conf.urls import url
from jscroll.wrappers import JScrollView

app_name = 'jscroll'
urlpatterns = [
    url(r'^jscroll-view/$', JScrollView.as_view(), name='jscroll-view'),
]




