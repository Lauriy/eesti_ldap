from __future__ import absolute_import, unicode_literals

import datetime

from celery import shared_task


@shared_task
def add(x, y):
    return x + y

def generate_estonian_personal_codes_for_birthdate(birthdate: datetime.date):
    if birthdate.year < 1900:
        male_female_digits = [1, 2]
    elif birthdate.year < 2000:
        male_female_digits = [3, 4]
    else:
        male_female_digits = [5, 6]
    birth_year_digits = [int(x) for x in str(birthdate.year)[2:]]
