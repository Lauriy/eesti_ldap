from django.contrib.postgres.fields import JSONField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class SkEeLdapQuery(models.Model):
    input = models.TextField(db_index=True, unique=True)
    response = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    modified = models.DateTimeField(auto_now=True)


# TODO: Fixtures
class BirthHospital(models.Model):
    name = models.CharField(max_length=255)
    latitude = models.FloatField(validators=[MinValueValidator(-85.05115), MaxValueValidator(85)])
    longitude = models.FloatField(validators=[MinValueValidator(-180), MaxValueValidator(180)])
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    modified = models.DateTimeField(auto_now=True)


class BirthDate(models.Model):
    actual_date = models.DateField()
    possible_national_ids = JSONField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    modified = models.DateTimeField(auto_now=True)
    search_exhausted = models.BooleanField(default=False)

    def __str__(self):
        return self.actual_date.isoformat()


class Person(models.Model):
    personal_code = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    birth_date = models.ForeignKey(BirthDate, on_delete='PROTECT', related_name='people')
    # birth_hospital = models.ForeignKey(BirthHospital, blank=True, null=True, on_delete='PROTECT')
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s %s - %s' % (self.first_name, self.last_name, self.birth_date)
