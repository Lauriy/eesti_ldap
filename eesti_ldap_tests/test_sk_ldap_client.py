import os

from eesti_ldap.sk_ldap_client import SkLdapClient

with open('/'.join([os.path.dirname(os.path.realpath(__file__)),
                    'fixtures/ldap_response_for_39004020251.txt'])) as f:
    ldap_response = f.read()


# @mock.patch('eesti_ldap.sk_ldap_client.SkLdapClient.search_for_personal_code', return_value=ldap_response)
def test_search_for_personal_code():
    client = SkLdapClient()
    response = client.search_for_personal_code('39004020251')

    print(response)
    assert (response == 1)
