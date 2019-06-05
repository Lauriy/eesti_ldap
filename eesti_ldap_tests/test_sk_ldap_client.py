import ast
import json
import os
from unittest import mock

from eesti_ldap.sk_ldap_client import SkLdapClient

with open('/'.join([os.path.dirname(os.path.realpath(__file__)),
                    'fixtures/ldap_response_for_first_50_codes_of_1990_04_02.txt'])) as f:
    ldap_response = f.read()


@mock.patch('eesti_ldap.sk_ldap_client.SkLdapClient.search_for_personal_codes', return_value=ldap_response)
def test_search_for_personal_code(patched_function):
    with open('/'.join([os.path.dirname(os.path.realpath(__file__)),
                        'fixtures/estonian_national_id_codes_for_1990_04_02.json'])) as f:
        codes_to_try = json.loads(f.read())

    client = SkLdapClient()
    response = client.search_for_personal_codes(codes_to_try[:50])

    assert (response == ldap_response)


def test_parse_ldap_result():
    # TODO: Extract to function
    parsed_personal_data = str(ast.literal_eval(ldap_response)[0][1]['cn'][0])[2:].split(',')
    first_name = parsed_personal_data[1].capitalize()
    last_name = parsed_personal_data[0].capitalize()

    assert first_name == 'Margus'
    assert last_name == 'Piispea'
