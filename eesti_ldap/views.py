import datetime
import logging

import bs4
import requests
from django.shortcuts import render, redirect

from eesti_ldap.forms import IdCheckQueryCreateForm
from eesti_ldap.models import IdCheckQuery

logger = logging.getLogger(__name__)

def frontpage(request):
    # FIXME: Just for testing
    # add.delay(4, 4)

    if request.method == 'POST':
        form = IdCheckQueryCreateForm(request.POST)
        if form.is_valid():
            obj, created = IdCheckQuery.objects.get_or_create(input=form.cleaned_data['input'])

            return redirect('my_birthday', year=obj.input.year, month=f'{obj.input.month:02d}',
                            day=f'{obj.input.day:02d}')
    elif request.method == 'GET':
        form = IdCheckQueryCreateForm()
    else:
        raise Exception('Bad request method')

    return render(request, 'eesti_ldap/frontpage.html', {
        'form': form
    })


def my_birthday(request, year, month, day):
    birthday = datetime.date(int(year), int(month), int(day))
    obj, created = IdCheckQuery.objects.get_or_create(input=birthday)

    response = requests.post('http://id-check.artega.biz/pin-ba.php', data={
        'dd': day,
        'mm': month,
        'yyyy': year,
        'sex': 'u'
    }, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
    })

    parsed_response = bs4.BeautifulSoup(response.text, 'html.parser')

    print(parsed_response.select('body > .cf > .tab'))

    return render(request, 'eesti_ldap/frontpage.html', {

    })
