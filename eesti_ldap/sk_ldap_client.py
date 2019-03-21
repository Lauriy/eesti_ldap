import ldap

l = ldap.initialize('ldap://ldap.sk.ee')
l.simple_bind_s('', '')
l.search_s('o=My Organisation, c=AU', ldap.SCOPE_SUBTREE, 'objectclass=*')
