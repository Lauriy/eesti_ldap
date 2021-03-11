import logging

from django.shortcuts import render

logger = logging.getLogger(__name__)


def frontpage(request):
    return render(request, 'eesti_ldap/frontpage.html', {

    })
