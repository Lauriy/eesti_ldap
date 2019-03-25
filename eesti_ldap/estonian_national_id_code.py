import datetime
from typing import List, Optional

from eesti_ldap.models import BirthHospital


def calculate_birth_year(personal_code: str) -> int:
    if personal_code[0] in ['1', '2']:
        year_digits = '18'
    elif personal_code[0] in ['3', '4']:
        year_digits = '19'
    else:
        year_digits = '20'

    return int(f'{year_digits}{personal_code[1:3]}')


def try_to_guess_birth_hospital(personal_code: str) -> Optional[BirthHospital]:
    birth_year = calculate_birth_year(personal_code)
    # https://et.wikipedia.org/wiki/Isikukood#Haigla_tunnus
    if birth_year > 2012:
        return None
    else:
        hospital_birth_order_number = personal_code[7:10].lstrip('0')
        if hospital_birth_order_number in range(1, 11):
            pass

    # TODO: Finish


def calculate_check_digit(personal_code: str) -> str:
    first_tier_weights = [1, 2, 3, 4, 5, 6, 7, 8, 9, 1]
    second_tier_weights = [3, 4, 5, 6, 7, 8, 9, 1, 2, 3]
    first_tier_weight_sum = sum([int(x) * first_tier_weights[i] for i, x in enumerate(personal_code[:10])])
    possible_check_digit = first_tier_weight_sum % 11
    if possible_check_digit != 10:
        return str(possible_check_digit)
    else:
        second_tier_weight_sum = sum([int(x) * second_tier_weights[i] for i, x in enumerate(personal_code[:10])])
        possible_check_digit = second_tier_weight_sum % 11
        if possible_check_digit != 10:
            return str(possible_check_digit)
        else:
            return '0'


def generate_codes_for_birthdate(birthdate: datetime.date) -> List[str]:
    if birthdate.year < 1900:
        male_female_digits = [1, 2]
    elif birthdate.year < 2000:
        male_female_digits = [3, 4]
    else:
        male_female_digits = [5, 6]
    birth_year_digits = str(birthdate.year)[2:]
    birth_month_digits = f'{birthdate.month:02d}'
    birth_day_digits = f'{birthdate.day:02d}'

    codes = []
    for male_female_digit in male_female_digits:
        for birth_order in range(0, 1000):
            birth_order_digits = f'{birth_order:03d}'
            partial_code = f'{male_female_digit}{birth_year_digits}{birth_month_digits}{birth_day_digits}{birth_order_digits}'
            check_digit = calculate_check_digit(partial_code)
            code_to_try = f'{partial_code}{check_digit}'
            codes.append(code_to_try)

    return codes
