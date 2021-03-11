from typing import List

import ldap
from django.conf import settings


class SkLdapClient:
    def __init__(self):
        self.ldap_client = ldap.initialize('ldaps://esteid.ldap.sk.ee')
        self.ldap_client.simple_bind_s('', '')

    def search_for_personal_codes(self, personal_codes: List[str]):
        if len(personal_codes) > settings.SK_LDAP_MAX_PAGE_SIZE:
            raise Exception(f'Cannot search for more than {settings.SK_LDAP_MAX_PAGE_SIZE} codes at once')

        query_parts = []
        for personal_code in personal_codes:
            query_parts.append(f'(serialNumber=PNOEE-{personal_code})')
        query_string = '(|' + ''.join(query_parts) + ')'

        return self.ldap_client.search_s('c=EE', ldap.SCOPE_SUBTREE, query_string)
