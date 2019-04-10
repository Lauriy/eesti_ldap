import os

from django.core.management.base import BaseCommand, CommandError

from eesti_ldap.sk_ldap_client import SkLdapClient


class Command(BaseCommand):
    help = 'Uses our client to search ldap.sk.ee for a single personal code'

    def add_arguments(self, parser):
        parser.add_argument('personal_code', nargs='+', type=str)

    def handle(self, *args, **options):
        client = SkLdapClient()
        for personal_code in options['personal_code']:
            try:
                result = client.search_for_personal_code(personal_code)
            except:
                raise CommandError('Failed to talk to ldap.sk.ee')

            with open('/'.join([os.path.dirname(os.path.realpath(__file__)),
                                'responses/ldap_response_for_%s.txt' % personal_code]), 'w') as f:
                f.write(str(result))
            self.stdout.write(self.style.SUCCESS('LDAP result: "%s"' % result))
