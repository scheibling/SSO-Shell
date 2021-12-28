from django.shortcuts import render
from django.http import HttpResponseBadRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from django.core import serializers as serial
from ssoshell_server.oidc_authentication import views as oidc_views
from ssoshell_server.device_auth.models import AuthRequest
import json, random, string

# Create your views here.
@csrf_exempt
def init(request):
    if not request.method == 'POST':
        return HttpResponseBadRequest()
    
    # Get POST JSON body
    body = request.body.decode('utf-8')
    
    # Generate random string
    token = "".join(random.choice(string.ascii_letters + string.digits) for _ in range(10))
    
    return HttpResponse(status=200, content_type='application/json', content=json.dumps({'token': token, 'url': request.build_absolute_uri('/device/open/%s' % token)}))
    
def open(request, token):
    if not request.method == 'GET':
        return HttpResponseBadRequest()
    
    if (len(token)) != 10:
        return HttpResponseBadRequest()
    
    request.session['token'] = token
    request.session['redirect'] = '/device/return'
    
    return HttpResponse(status=200, content_type='text/html', content=render(request, 'authenticate.html'))

def method(request, methodname):
    if not request.method == 'GET':
        return HttpResponseBadRequest()
    
    if methodname not in ('oidc', 'saml'):
        return HttpResponseBadRequest()
    
    return oidc_views.login(request, '/device/return')
    
def retn(request):
    if not request.session.get('token'):
        return HttpResponseBadRequest()
    
    arr = {}
    for key in request.session.keys():
        arr[key] = request.session.get(key)
    
    db_q = AuthRequest(
        user_id=request.session.get('_auth_user_id'),
        token=request.session.get('token'),
        verified=True
    )
    try:
        db_q.save()
    except IntegrityError as e:
        return HttpResponseBadRequest(content="You have already authenticated this token. Please generate a new link with the commandline utility.")
    arr['database_id'] = db_q.id
    
    return HttpResponse(status=200, content_type='application/json', content=json.dumps(arr))

def callback(request, token):
    print(token)
    
    dbase = AuthRequest.objects.filter(token=token)
    
    print(serial.serialize('json', dbase))
    
    return HttpResponse(status=200, content_type='application/json', content=serial.serialize('json', dbase))