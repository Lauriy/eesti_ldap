from django.contrib import admin
from django.urls import path, re_path

from eesti_ldap.views import my_birthday, frontpage

urlpatterns = [
    path('', frontpage),
    re_path(r'^birthday/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/$', my_birthday, name='my_birthday'),
    path('admin/', admin.site.urls),
]
