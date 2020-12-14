#from django.shortcuts import render
import requests
import time
import six
from django.db import DatabaseError
from django.shortcuts import render,redirect
from rest_framework import viewsets
from django.conf import settings
from .serializers import AccountSerializer, TagSerializer, TransactionSerializer
from .models import Account, Tag, Transaction, TIPOS_TAG, CAT_PRINCIPALES
from .forms import AccountForm, TagForm, TransactionForm
from django.forms.models import modelformset_factory
import pprint
import re
import math

# Create your views here.
requests.packages.urllib3.disable_warnings()


def buxfer_login(request):
    ''' performs the login in the buxfer api and returns the token and a status text '''
    response = requests.get("%s/login?userid=%s" \
                            "&password=%s" % (settings.BUXFER_CONN['url'], settings.BUXFER_CONN['user'], settings.BUXFER_CONN['pass']))

    if response.status_code != 200:
        return (None, get_err_msg(response))

    token = response.json()
    return (token['response']['token'], 'ok')


def buxfer_get_token(request):
    '''  gets the the Buxfer token from the request object or doing a login in buxfer api '''
    status = 'ok'
    token = request.session.get('buxfer_token', None)
    if not token:
        (token, status) = buxfer_login(request)
    return (token, status)


def get_err_msg(response):
    ''' Formats the error message of a requests response'''
    data = response.json()
    err_type = data['error']['type']
    err_msg = data['error']['message']
    return "({}) {} {}".format(response.status_code, err_type, err_msg)


def buxfer_api_fetch(request, resource, page=None):
    '''
    Fetches a resource from the buxfer api
    :param request: django request object
    :param resource:
    :return: dictionary containing the data of the request in json and a string inidcating 'ok' or 'error'
    '''
    attempt_num = 0  # keep track of how many times we've retried
    while attempt_num < settings.BUXFER_CONN['max_retiries']:
        (token, status) = buxfer_get_token(request)
        if not token:
            return {'data': None, 'status': 'Buxfer Login Error: {}'.format(status)}
        url = "%s/%s?token=%s" % (settings.BUXFER_CONN['url'],
                                  resource, token)
        if page:
            url = '{}&page={}'.format(url, page)
        response = requests.get(url, timeout=10)
        print(url)
        if response.status_code == 200:
            data = response.json()
            return {'data': data, 'status': 'ok' }
        else:
            attempt_num += 1
            # You can probably use a logger to log the error here
            time.sleep(5)  # Wait for 5 seconds before re-trying

    err_msg = get_err_msg(response)
    return {'data': None, 'status': 'Error: {}'.format(err_msg) }

def has_changed(record, data):
    for key in data:
        #print(getattr(record, key, None))
        if data[key] != getattr(record, key, None):
            return True
    return False

def save_serializer(actionResponseData, keys, queryset, serializerClass):
    result = []
    serialized_keys = []
    for acc in actionResponseData:
        serializer = None
        #pprint.pprint(acc)
        # si uso many=True en el serializer, graba solo algunos
        if acc['id'] in keys:
            db_rec = queryset[acc['id']]
            if has_changed(db_rec, acc):
                serializer = serializerClass(db_rec, data=acc)
            else:
                result.append('{} not changed'.format(acc['id']))
        else:
            serializer = serializerClass(data=acc)

        if serializer:
            if serializer.is_valid():
                serialized_keys.append(acc['id'])
                embed = serializer.save()
                result.append(embed)
            else:
                result.append(serializer.errors)
    # delete the ones that are not in buxfer anymore
    # to_delete = [x for x in keys if x not in serialized_keys]
    # modelClass.objects.filter(pk__in=to_delete).delete()

    return result

def data_import(request, action, modelClass, serializerClass, formClass=None):
    ''' Imports data from buxfer '''
    result = []
    to_delete = None
    formSetClass = modelformset_factory(modelClass, form=formClass, extra=0, can_delete=False)

    if request.method != 'POST':
        data = buxfer_api_fetch(request, action)
        if data['status'] == 'ok':
            queryset = dict([(x.id, x) for x in modelClass.objects.all()])
            keys = list(six.iterkeys(queryset))
            #import pdb; pdb.set_trace()

            result = save_serializer(data['data']['response'][action], keys, queryset, serializerClass)

            if action == 'transactions':
                numTransactions = data['data']['response']['numTransactions']
                print(numTransactions)
                for page in range(2, math.ceil(int(numTransactions) / 25) + 1):
                    data = buxfer_api_fetch(request, action, page)
                    result += save_serializer(data['data']['response'][action], keys, queryset, serializerClass)
            print(result)
            # import pdb;pdb.set_trace()
            ids = [x.id for x in result if hasattr(x, 'id')] # not isinstance(x, str)]
            if formClass and ids:
                queryset = modelClass.objects.filter(id__in=ids)
                formset = formSetClass(queryset = queryset)
                qData = zip(list(queryset), list(formset))
            else:
                formset = None
                qData = None
    else:
        data = {'status': 'No Changes.'}
        if formClass:
            # regex_list=['the', 'an?']
            # regex_list_compiled=[re.compile("^"+i+"$") for i in regex_list]
            # extractddicti= {k:v for k,v in dicti.items() if any (re.match(regex,k) for regex in regex_list_compiled)}
            pattern = 'form-[0-9]+-id'
            ids = [value for key, value in request.POST.items() if re.search(pattern, key)]
            queryset = modelClass.objects.filter(id__in=ids)
            formset = formSetClass(request.POST, request.FILES)
            qData = zip(list(queryset), list(formset))
            # import pdb; pdb.set_trace()
            if formset.is_valid():
                # do something with the formset.cleaned_data
                for form in formset:
                    if form.is_valid() and form.changed_data:
                        try:
                            #if form.cleaned_data.get('DELETE') and form.instance.pk:
                            #    form.instance.delete()
                            #else:
                            form.save()
                            data['status'] = "Saved."
                        except DatabaseError as e:
                            data['status'] = "Error: {}".format(e)

    qFieldNames = modelClass().get_fieldNames()
    return render(request, "buxfer_api/data_imported.html", {'status': data['status'], 'data': result, 'action': action,
                                                             'deleted': to_delete, 'qdata': qData, 'qFieldNames': qFieldNames,
                                                             'formset': formset})

def accounts_import(request):
    ''' Imports the accounts'''
    action = 'accounts'
    serializerClass = AccountSerializer
    model = Account
    formSetClass = AccountForm
    return data_import(request, action, model, serializerClass, formSetClass)

def tags_import(request):
    ''' Imports the accounts'''
    action = 'tags'
    serializerClass = TagSerializer
    model = Tag
    formSetClass = TagForm
    return data_import(request, action, model, serializerClass, formSetClass)

def transactions_import(request):
    ''' Imports the accounts'''
    accounts_import(request)
    tags_import(request)
    action = 'transactions'
    serializerClass = TransactionSerializer
    model = Transaction
    formSetClass = TransactionForm
    return data_import(request, action, model, serializerClass, formSetClass)

def clasificar_transacciones(anio, mes):
    if anio and mes:
        transactions = Transaction.objects.filter(normalizedDate__year=anio, normalizedDate__month=mes).order_by('-normalizedDate')
    elif anio:
        transactions = Transaction.objects.filter(normalizedDate__year=anio).order_by('-normalizedDate')
    else:
        transactions = Transaction.objects.order_by('-normalizedDate')

    data = {}
    total = 0
    tipos_tag = {}

    for key, value in TIPOS_TAG:
        data[value] = {}
        data[value]['data'] = {}
        data[value]['total'] = 0
        tipos_tag[key] = value

    categorias = dict([ x for x in CAT_PRINCIPALES ])

    #import pdb;pdb.set_trace()
    for transaction in transactions:
        tags = transaction.tags.all()
        if tags:
            tag = tags[0]
            if tag.tipo_tag and tag.categoria and tag.categoria in categorias:
                tiponame = tipos_tag[tag.tipo_tag]
                catname = categorias[tag.categoria]
                if catname not in data[tiponame]['data']:
                    data[tiponame]['data'][catname] = {}
                    data[tiponame]['data'][catname]['data'] = {}
                    data[tiponame]['data'][catname]['total'] = 0
                if tag.name not in data[tiponame]['data'][catname]['data']:
                    data[tiponame]['data'][catname]['data'][tag.name] = {}
                    data[tiponame]['data'][catname]['data'][tag.name]['data'] = []
                    data[tiponame]['data'][catname]['data'][tag.name]['total'] = 0
                data[tiponame]['data'][catname]['data'][tag.name]['data'].append(transaction)
                data[tiponame]['data'][catname]['data'][tag.name]['total'] += transaction.amount
                data[tiponame]['data'][catname]['total'] += transaction.amount
                data[tiponame]['total'] += transaction.amount
                total += transaction.amount

    # import pdb; pdb.set_trace()
    show_data = [ (x, data[x]) for x in ['Ingreso', 'Gasto', 'Activo', 'Pasivo']]

    return show_data, total

def cuadro_activos(request, anio=None, mes=None):
    ''' Muestra tabla de activos, pasivos, ingresos y gastos '''

    show_data, total = clasificar_transacciones(anio, mes)
    #pprint.pprint(show_data)

    return render(request, "buxfer_api/cuadro_activos.html", {'data': show_data, 'total':total})

