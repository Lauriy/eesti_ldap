import bs4
import requests

from eesti_ldap.models import IdCheckQuery


class IdCheckClient:
    def retrieve_valid_id_codes(self, id_check_query: IdCheckQuery):
        response = requests.post('http://id-check.artega.biz/pin-ba.php', data={
            'dd': id_check_query.dd,
            'mm': id_check_query.mm,
            'yyyy': id_check_query.yyyy,
            'sex': 'u'
        })

        parsed_response = bs4.BeautifulSoup(response.text, 'html.parser')

        # id_check_query.response = response.text
        # id_check_query.save()

        return id_check_query
