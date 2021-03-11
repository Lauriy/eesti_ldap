from django.contrib import admin
from django.urls import path

from eesti_ldap.views import frontpage

urlpatterns = [
    path('', frontpage),
    path('admin/', admin.site.urls),
]
