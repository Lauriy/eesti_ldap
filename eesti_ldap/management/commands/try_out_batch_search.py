import ast
import datetime
import json
from math import ceil
from time import sleep

from django.core.management.base import BaseCommand
from nameparser import HumanName

from eesti_ldap.estonian_national_id_code import generate_codes_for_birthdate
from eesti_ldap.models import SkEeLdapQuery, Person, BirthDate
from eesti_ldap.sk_ldap_client import SkLdapClient
from django.conf import settings


# TODO: Run a similar task with Celery beat every 24 hours that queues smaller 'ask LDAP' tasks 1 every 10 seconds with an expiry of 23 hours 59 minutes
class Command(BaseCommand):
    help = 'Uses our client to search ldap.sk.ee for a set of personal codes to determine how quick we get banned'

    def add_arguments(self, parser):
        parser.add_argument('birthdate', nargs=1, type=str)

    def handle(self, *args, **options):
        input_parts = [int(x) for x in options['birthdate'][0].split('-')]
        birthdate, created = BirthDate.objects.get_or_create(actual_date=datetime.date(year=input_parts[0],
                                                                                       month=input_parts[1],
                                                                                       day=input_parts[2]))
        client = SkLdapClient()
        if not birthdate.possible_national_ids:
            personal_codes = generate_codes_for_birthdate(birthdate.actual_date)
        else:
            personal_codes = json.loads(birthdate.possible_national_ids)
        personal_codes.sort()
        page = 0
        page_size = settings.SK_LDAP_MAX_PAGE_SIZE
        max_page = ceil(float(len(personal_codes)) / float(page_size))
        while page < max_page:
            codes_to_ask_about = personal_codes[page * page_size:(page + 1) * page_size]
            cached, created = SkEeLdapQuery.objects.get_or_create(input=', '.join(codes_to_ask_about))
            if cached.response is None:
                result = str(client.search_for_personal_codes(codes_to_ask_about))
                cached.response = json.dumps(result)
                cached.save()
                sleep(5)
            else:
                result = json.loads(cached.response)
            for entry in ast.literal_eval(result):
                person_data = entry[1]['cn'][0].decode('utf-8').split(',')
                name = HumanName(' '.join([person_data[1], person_data[0]]))
                name.capitalize(force=True)
                person, created = Person.objects.get_or_create(personal_code=person_data[2], birth_date=birthdate)
                if created:
                    person.first_name = ' '.join([name.first, name.middle])
                    person.last_name = name.last
                    person.save()
            page += 1
