import ldap


class SkLdapClient:
    def __init__(self):
        self.ldap_client = ldap.initialize('ldap://ldap.sk.ee')
        self.ldap_client.simple_bind_s('', '')

    def search_for_personal_code(self, personal_code: str):
        return self.ldap_client.search_s('c=EE', ldap.SCOPE_SUBTREE, f'serialNumber={personal_code}')
