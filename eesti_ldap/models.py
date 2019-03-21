from django.db import models


class IdCheckQuery(models.Model):
    # DD_CHOICES = [(f'{x:02d}', f'{x:02d}') for x in range(1, 32)]
    # MM_CHOICES = [(f'{x:02d}', f'{x:02d}') for x in range(1, 13)]
    #
    # dd = models.CharField(choices=DD_CHOICES, max_length=2)
    # mm = models.CharField(choices=MM_CHOICES, max_length=2)
    # yyyy = models.PositiveSmallIntegerField(
    #     validators=[MinValueValidator(1850), MaxValueValidator(datetime.datetime.now().year)])
    input = models.DateField(unique=True)
    response = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    modified = models.DateTimeField(auto_now=True)


class SkEeLdapQuery(models.Model):
    pass
