from django.contrib import admin

from eesti_ldap.models import BirthDate, Person

admin.site.register(BirthDate)
admin.site.register(Person)
# admin.site.register(BirthHospital)
