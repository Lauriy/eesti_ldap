import ast
import datetime
import json
from math import ceil
from time import sleep

from django.conf import settings
from django.core.management.base import BaseCommand

from eesti_ldap.estonian_national_id_code import generate_codes_for_birthdate
from eesti_ldap.models import SkEeLdapQuery, Person, BirthDate
from eesti_ldap.sk_ldap_client import SkLdapClient


class Command(BaseCommand):
    help = 'Scrape a whole year worth of people'

    def add_arguments(self, parser):
        parser.add_argument('year', nargs=1, type=str)

    def handle(self, *args, **options):
        year = int(options['year'][0])
        current = datetime.date(year=year, month=1, day=1)
        end = datetime.date(year=year, month=12, day=31)
        delta = datetime.timedelta(days=1)
        client = SkLdapClient()
        while current <= end:
            print(current)
            birthdate, created = BirthDate.objects.get_or_create(actual_date=datetime.date(year=current.year,
                                                                                           month=current.month,
                                                                                           day=current.day))
            if not birthdate.possible_national_ids:
                personal_codes = generate_codes_for_birthdate(birthdate.actual_date)
                personal_codes.sort()
                birthdate.possible_national_ids = json.dumps(personal_codes)
                birthdate.save()
            else:
                personal_codes = json.loads(birthdate.possible_national_ids)
                personal_codes.sort()
            print(personal_codes)
            page = 0
            page_size = settings.SK_LDAP_MAX_PAGE_SIZE
            max_page = ceil(float(len(personal_codes)) / float(page_size))
            while page < max_page:
                codes_to_ask_about = personal_codes[page * page_size:(page + 1) * page_size]
                print(codes_to_ask_about)
                cached, created = SkEeLdapQuery.objects.get_or_create(input=', '.join(codes_to_ask_about))
                if cached.response is None:
                    result = str(client.search_for_personal_codes(codes_to_ask_about))
                    cached.response = json.dumps(result)
                    cached.save()
                    sleep(settings.SK_LDAP_QUERY_COOLDOWN_SECONDS)
                else:
                    result = json.loads(cached.response)
                for entry in ast.literal_eval(result):
                    person_data = entry[1]['cn'][0].decode('utf-8').split(',')
                    print(person_data)
                    person, created = Person.objects.get_or_create(personal_code=person_data[2], birth_date=birthdate)
                    if created:
                        person.last_name = person_data[0]
                        person.first_name = person_data[1]
                        person.save()
                page += 1
            birthdate.search_exhausted = True
            birthdate.save()
            current += delta
