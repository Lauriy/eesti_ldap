from __future__ import absolute_import, unicode_literals

import json
from time import sleep
from typing import List, Optional

from asgiref.sync import async_to_sync
from celery import shared_task, group, subtask
from channels.layers import get_channel_layer
from django.db import transaction

from eesti_ldap.estonian_national_id_code import generate_codes_for_birthdate
from eesti_ldap.models import Person, BirthDate
from eesti_ldap.sk_ldap_client import SkLdapClient


@shared_task
def calculate_possible_national_ids_for_birthdate(birth_date_pk: int) -> List[str]:
    with transaction.atomic():
        birth_date = BirthDate.objects.filter(pk=birth_date_pk).select_for_update().get()
        if not birth_date.possible_national_ids:
            codes = generate_codes_for_birthdate(birth_date.actual_date)
            birth_date.possible_national_ids = json.dumps(codes)
            birth_date.save()
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                'birthdate_%d_%d_%d' % (birth_date.year, birth_date.month, birth_date.year.day), {
                    'type': 'birthdate.message',
                    'message': birth_date.possible_national_ids
                })
        else:
            codes = json.loads(birth_date.possible_national_ids)

    return codes


@shared_task
def retrieve_batch_of_people_from_ldap(personal_code: List[str]) -> List[str]:
    # TODO: Does this waste memory? SASL attempts?
    return 'test'
    # sk_client = SkLdapClient()
    # ldap_response = sk_client.search_for_personal_code(personal_code)
    # if ldap_response:
    # return ldap_response


@shared_task
def dmap(iterable, callback):
    callback = subtask(callback)

    return group(callback.clone([arg, ]) for arg in iterable)()
