from __future__ import absolute_import, unicode_literals

import json
from math import ceil
from typing import List

from celery import shared_task, subtask, group
from django.conf import settings
from django.db import transaction

from eesti_ldap.estonian_national_id_code import generate_codes_for_birthdate
from eesti_ldap.models import BirthDate


@shared_task
def enqueue_personal_code_query_batches():
    birthdates_requiring_work = BirthDate.objects.filter(search_exhausted=False)
    seconds_booked = 0
    for birthdate in birthdates_requiring_work:
        if not birthdate.possible_national_ids:
            personal_codes = generate_codes_for_birthdate(birthdate.actual_date)
            birthdate.possible_national_ids = personal_codes
            birthdate.save()
        else:
            personal_codes = json.loads(birthdate.possible_national_ids)
        personal_codes.sort()
        page = 0
        page_size = settings.SK_LDAP_MAX_PAGE_SIZE
        max_page = ceil(float(len(personal_codes)) / float(page_size))
        this_batch = []
        while page < max_page:
            this_batch.append(personal_codes[page * page_size:(page + 1) * page_size])
            seconds_booked += settings.SK_LDAP_QUERY_COOLDOWN_SECONDS
            page += 1
        if seconds_booked <= (
                settings.SK_LDAP_QUERIES_BATCH_INTERVAL_SECONDS
                - settings.SK_LDAP_QUERIES_BATCH_INTERVAL_SAFETY_SECONDS):
            # We have enough time left to book this whole batch
            batch_size = len(this_batch)
            for index, set_of_codes in enumerate(this_batch):
                if index == (batch_size - 1):
                    # Last batch
                    retrieve_batch_of_people_from_ldap.apply_async((set_of_codes, True), )
                else:
                    retrieve_batch_of_people_from_ldap.apply_async((set_of_codes, False), )
        else:
            # We're done for this interval
            break


@shared_task
def calculate_possible_national_ids_for_birthdate(birth_date_pk: int) -> List[str]:
    with transaction.atomic():
        birth_date = BirthDate.objects.filter(pk=birth_date_pk).select_for_update().get()
        codes = generate_codes_for_birthdate(birth_date.actual_date)
        birth_date.possible_national_ids = json.dumps(codes)
        birth_date.save()

    return codes


@shared_task
def retrieve_batch_of_people_from_ldap(personal_code: List[str], is_last_batch: bool) -> List[str]:
    return ['test']


# Can be used to link an array of follow-up tasks on completion of the 'mother'-task
@shared_task
def dmap(iterable, callback):
    callback = subtask(callback)

    return group(callback.clone([arg, ]) for arg in iterable)()
