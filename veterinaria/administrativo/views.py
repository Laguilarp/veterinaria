import sys
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db import transaction

@login_required(redirect_field_name='next', login_url='/login/')
@transaction.atomic()
def menuprincipal(request):
    global ex
    data = {}
    try:
        data['titulo'] = 'Menú principal'
        return render(request, "base.html", data)
    except Exception as ex:
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
