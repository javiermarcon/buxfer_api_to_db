#from django.shortcuts import render
import requests
import time
from django.shortcuts import render,redirect

# Create your views here.
requests.packages.urllib3.disable_warnings()

MAX_RETRIES = 5  # Arbitrary number of times we want to try
BUXFER_BASE_URL = "https://www.buxfer.com/api"
USER = ""
PASS = ""


def buxfer_login(request):
    ''' performs the login in the buxfer api and returns the token and a status text '''
    response = requests.get("%s/login?userid=%s" \
                            "&password=%s" % (BUXFER_BASE_URL, USER, PASS))

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
    return "({}) {}" - format(response.status_code, err_type)


def buxfer_api_fetch(request, resource):
    '''
    Fetches a resource from the buxfer api
    :param request: django request object
    :param resource:
    :return: dictionary containing the data of the request in json and a string inidcating 'ok' or 'error'
    '''
    attempt_num = 0  # keep track of how many times we've retried
    while attempt_num < MAX_RETRIES:
        (token, status) = buxfer_get_token(request)
        if not token:
            return {'data': 'Buxfer Login Error', 'status': 'error'}
        url = "%s/%s?token=%s" % (BUXFER_BASE_URL,
                                  resource, token)
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return {'data': data, 'status': 'ok' }
        else:
            attempt_num += 1
            # You can probably use a logger to log the error here
            time.sleep(5)  # Wait for 5 seconds before re-trying

    err_msg = get_err_msg(response)
    return {'data': err_msg, 'status': 'error' }


def accounts_import(request):
    ''' Imports the transactions from buxfer '''
    data = buxfer_api_fetch(request, 'accounts')
    if data['status'] == 'ok':
        for acc in data['data']['response']['accounts']:
            print(acc)
    return render(request, "accounts_imported.html")