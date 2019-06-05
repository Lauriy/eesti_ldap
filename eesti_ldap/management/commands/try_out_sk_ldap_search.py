import os

from django.core.management.base import BaseCommand

from eesti_ldap.sk_ldap_client import SkLdapClient


class Command(BaseCommand):
    help = 'Uses our client to search esteid.ldap.sk.ee for a single personal code'

    def add_arguments(self, parser):
        parser.add_argument('personal_codes', nargs='+', type=str)

    def handle(self, *args, **options):
        client = SkLdapClient()
        result = client.search_for_personal_codes(options['personal_codes'])
        with open('/'.join([os.path.dirname(os.path.realpath(__file__)), 'responses/last_ldap_response.txt']),
                  'w') as f:
            f.write(str(result))
        self.stdout.write(self.style.SUCCESS('LDAP result: "%s"' % result))
