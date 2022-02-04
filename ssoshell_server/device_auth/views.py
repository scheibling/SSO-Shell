from django.shortcuts import render
from django.http import HttpResponseBadRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from django.contrib.auth.models import Group as UserGroup
from django.core import serializers as serial
from django.conf import settings
from ssoshell_server.oidc_authentication import views as oidc_views
from ssoshell_server.device_auth.models import AuthRequest, AuthCompleted
from ssoshell_server.ssh_ca.actions import sign_key
from ssoshell_server.host.models import UserHostPermission, UserHostgroupPermission
import json, random, string

# Create your views here.
@csrf_exempt
def init(request):
    if not request.method == 'POST':
        return HttpResponseBadRequest()
    
    # Get POST JSON body
    body = request.body.decode('utf-8')
    print(body)
    
    # Generate random string
    token = "".join(random.choice(string.ascii_letters + string.digits) for _ in range(10))
    
    # Insert auth request into database
    db_q = AuthRequest(
        token=token,
        public_key=body
    )
    
    try:
        db_q.save()
    except IntegrityError as e:
        return HttpResponseBadRequest(content=e)
    
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
    
    request.session['method'] = methodname
    
    return oidc_views.login(request, '/device/return')
    
def retn(request):
    if not request.session.get('token'):
        return HttpResponseBadRequest(content='No token in session')
    
    try:
        auth_request = AuthRequest.objects.get(token=request.session.get('token'))
    except AuthRequest.DoesNotExist as e:
        return HttpResponseBadRequest(content=e)
      
    subject = request.session.get(settings.SSH_CA_CERT_SUBJECT_OIDC)
    if (request.session.get('method') == 'oidc'):
        subject = request.session.get('openid', {}).get(settings.SSH_CA_CERT_SUBJECT_OIDC)
    if (request.session.get('method') == 'saml'):
        subject = request.session.get('saml', {}).get(settings.SSH_CA_CERT_SUBJECT_SAML)
    
    principals = [subject]
    
    # Get user direct server principals
    host_principals = UserHostPermission.objects.filter(user=request.user.id)
    
    # Get user group principals
    ugr_principals = UserGroup.objects.filter(user=request.user)
    
    # Get user hostgroup principals
    hgr_principals = UserHostgroupPermission.objects.filter(user=request.user.id)
    
    for item in host_principals:
        principals.append(item.host.hostname)
        
    for item in ugr_principals: 
        principals.append(f'ugr-{item.name}'.replace(' ', '-'))
    
    for item in hgr_principals:
        principals.append(f'hgr-{item.hostgroup.group_slug}')
    
    principals = ','.join(principals)
    
    # try:
    auth_completed = AuthCompleted(
        token=auth_request.token,
        user_id=request.session.get('_auth_user_id'),
        certificate_subject=subject,
        certificate_principals=principals,
        signed_key='None'
    )
    auth_completed.save()       
    
    auth_completed = AuthCompleted.objects.get(token=auth_request.token)
    
    # Sign the key
    signed = sign_key(auth_request.public_key, subject, principals, auth_completed.serial)
    
    auth_completed.signed_key = signed
    auth_completed.save()
    
    request.session.flush()
    
    return HttpResponse(status=200, content_type='text/html', content="You have now successfully authenticated. You can close this window and go back to your SSH Shell.")

@csrf_exempt
def callback(request, token):
    try:
        auth_object = AuthCompleted.objects.get(token=token)
    except AuthCompleted.DoesNotExist as e:
        return HttpResponseBadRequest(content=e)    
        
    return HttpResponse(status=200, content_type='text/plain', content=auth_object.signed_key)