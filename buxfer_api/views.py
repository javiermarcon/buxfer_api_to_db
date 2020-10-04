#from django.shortcuts import render
import requests
import time
import six
from django.shortcuts import render,redirect
from rest_framework import viewsets
from django.conf import settings
from .serializers import AccountSerializer, TagSerializer, TransactionSerializer
from .models import Account, Tag, Transaction
import pprint
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


def buxfer_api_fetch(request, resource):
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

def data_import(request, action, modelClass, serializerClass):
    ''' Imports data from buxfer '''
    data = buxfer_api_fetch(request, action)
    result = []
    if data['status'] == 'ok':
        queryset = dict([(x.id, x) for x in modelClass.objects.all()])
        keys = list(six.iterkeys(queryset))
        serialized_keys = []
        #import pdb; pdb.set_trace()
        if action == 'transactions':
            numTransactions = data['data']['response']['numTransactions']
            print(numTransactions)
        for acc in data['data']['response'][action]:
            serializer = None
            pprint.pprint(acc)
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
        to_delete = [x for x in keys if x not in serialized_keys]
        modelClass.objects.filter(pk__in=to_delete).delete()
    return render(request, "buxfer_api/data_imported.html", {'status': data['status'], 'data': result, 'action': action, 'deleted': to_delete})

def accounts_import(request):
    ''' Imports the accounts'''
    action = 'accounts'
    serializerClass = AccountSerializer
    model = Account
    return data_import(request, action, model, serializerClass)

def tags_import(request):
    ''' Imports the accounts'''
    action = 'tags'
    serializerClass = TagSerializer
    model = Tag
    return data_import(request, action, model, serializerClass)

def transactions_import(request):
    ''' Imports the accounts'''
    accounts_import(request)
    tags_import(request)
    action = 'transactions'
    serializerClass = TransactionSerializer
    model = Transaction
    return data_import(request, action, model, serializerClass)
