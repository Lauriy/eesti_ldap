import ast
import os
from unittest import mock

from eesti_ldap.sk_ldap_client import SkLdapClient

with open('/'.join([os.path.dirname(os.path.realpath(__file__)),
                    'fixtures/ldap_response_for_39004020251.txt'])) as f:
    ldap_response = f.read()


@mock.patch('eesti_ldap.sk_ldap_client.SkLdapClient.search_for_personal_code', return_value=ldap_response)
def test_search_for_personal_code():
    client = SkLdapClient()
    response = client.search_for_personal_code('39004020251')

    assert (response == ldap_response)


def test_parse_ldap_result():
    # TODO: Extract to function
    parsed_personal_data = str(ast.literal_eval(ldap_response)[0][1]['cn'][0])[2:].split(',')
    first_name = parsed_personal_data[1].capitalize()
    last_name = parsed_personal_data[0].capitalize()

    assert first_name == 'Lauri'
    assert last_name == 'Elias'