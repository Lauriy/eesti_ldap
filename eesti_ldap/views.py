import datetime
import logging

# import bs4
# import requests
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.shortcuts import render, redirect

from eesti_ldap.forms import IdCheckQueryCreateForm
# from eesti_ldap.models import IdCheckQuery
from eesti_ldap.models import BirthDate
from eesti_ldap.tasks import calculate_possible_national_ids_for_birthdate, dmap

logger = logging.getLogger(__name__)


def frontpage(request):
    # FIXME: Just for testing
    # add.delay(4, 4)

    if request.method == 'POST':
        form = IdCheckQueryCreateForm(request.POST)
        if form.is_valid():
            return redirect('my_birthday', year=form.cleaned_data['input'].year,
                            month=f'{form.cleaned_data["input"].month:02d}',
                            day=f'{form.cleaned_data["input"].day:02d}')
    elif request.method == 'GET':
        form = IdCheckQueryCreateForm()
    else:
        raise Exception('Bad request method')

    # channel_layer = get_channel_layer()
    # async_to_sync(channel_layer.group_send)(
    #     'birthdate_1990_4_1', {
    #         'type': 'birthdate.message',
    #         'message': '12345'
    #     })

    return render(request, 'eesti_ldap/frontpage.html', {
        'form': form
    })


def my_birthday(request, year, month, day):
    # For validation
    birthdate = datetime.date(year=int(year), month=int(month), day=int(day))
    obj, created = BirthDate.objects.get_or_create(actual_date=birthdate)
    if not obj or not obj.possible_national_ids:
        # Always enqueue ID generation code if we don't have them generated already
        calculate_possible_national_ids_for_birthdate.apply_async((obj.pk,))

        # calculate_possible_national_ids_for_birthdate.apply_async((obj.pk,), link=dmap.s(retrieve_person_from_ldap.s()))

    return render(request, 'eesti_ldap/my_birthday.html', {
        'year': birthdate.year,
        'month': f'{birthdate.month:02d}',
        'day': f'{birthdate.day:02d}',
    })
