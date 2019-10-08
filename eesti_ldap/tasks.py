from __future__ import absolute_import, unicode_literals

import json
from math import ceil
from typing import List

from celery import shared_task
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

            # cached, created = SkEeLdapQuery.objects.get_or_create(input=', '.join(codes_to_ask_about))
            # if cached.response is None:
            #     result = str(client.search_for_personal_codes(codes_to_ask_about))
            #     cached.response = json.dumps(result)
            #     cached.save()
            #     sleep(5)
            # else:
            #     result = json.loads(cached.response)
            # for entry in ast.literal_eval(result):
            #     person_data = entry[1]['cn'][0].decode('utf-8').split(',')
            #     name = HumanName(' '.join([person_data[1], person_data[0]]))
            #     name.capitalize(force=True)
            #     person, created = Person.objects.get_or_create(personal_code=person_data[2], birth_date=birthdate)
            #     if created:
            #         person.first_name = ' '.join([name.first, name.middle])
            #         person.last_name = name.last
            #         person.save()


@shared_task
def calculate_possible_national_ids_for_birthdate(birth_date_pk: int) -> List[str]:
    with transaction.atomic():
        birth_date = BirthDate.objects.filter(pk=birth_date_pk).select_for_update().get()
        codes = generate_codes_for_birthdate(birth_date.actual_date)
        birth_date.possible_national_ids = json.dumps(codes)
        birth_date.save()
        # channel_layer = get_channel_layer()
        # async_to_sync(channel_layer.group_send)(
        #     'birthdate_%d_%d_%d' % (birth_date.actual_date.year, birth_date.actual_date.month, birth_date.actual_date.day), {
        #         'type': 'birthdate.message',
        #         'message': birth_date.possible_national_ids
        #     })

    return codes


@shared_task
def retrieve_batch_of_people_from_ldap(personal_code: List[str], is_last_batch: bool) -> List[str]:
    return ['test']
    # TODO: Does this waste memory? SASL attempts?
    # sk_client = SkLdapClient()
    # ldap_response = sk_client.search_for_personal_code(personal_code)
    # if ldap_response:
    # return ldap_response

# Can be used to link an array of follow-up tasks on completion of the 'mother'-task
# @shared_task
# def dmap(iterable, callback):
#     callback = subtask(callback)
#
#     return group(callback.clone([arg, ]) for arg in iterable)()
