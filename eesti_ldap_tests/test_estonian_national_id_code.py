import datetime
import json
import os

import pytest

from eesti_ldap.estonian_national_id_code import generate_codes_for_birthdate, calculate_check_digit, \
    calculate_birth_year


@pytest.mark.parametrize(('national_id_code', 'expected_year'), [
    ('39004020251', '1990'),
    ('38401180294', '1984'),
    ('61703300095', '2017')
])
def test_calculate_birth_year(national_id_code: str, expected_year: str):
    assert (calculate_birth_year(national_id_code) == expected_year)


@pytest.mark.parametrize(('national_id_code', 'expected_digit'), [
    ('39004020251', '1'),
    ('38401180294', '4'),
    ('61703300095', '5')
])
def test_calculate_check_digit(national_id_code: str, expected_digit: str):
    assert (calculate_check_digit(national_id_code) == expected_digit)


def test_generate_codes_for_birthdate():
    test_birth_date = datetime.date(year=1990, month=4, day=2)
    with open('/'.join([os.path.dirname(os.path.realpath(__file__)),
                        'fixtures/estonian_national_id_codes_for_1990_04_02.json'])) as f:
        # Taken from http://id-check.artega.biz/pin-ba.php
        expected_codes = json.loads(f.read())
        assert (generate_codes_for_birthdate(test_birth_date) == expected_codes)
