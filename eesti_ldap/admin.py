from django.contrib import admin

from eesti_ldap.models import BirthHospital, BirthDate

admin.site.register(BirthDate)
admin.site.register(BirthHospital)
