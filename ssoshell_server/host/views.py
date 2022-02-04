import json
import uuid
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseBadRequest
from django.conf import settings
from django.contrib.auth.models import Group as UserGroup
from .models import Host, HostGroupAssignment, GroupHostPermission

@csrf_exempt
def bootstrap_host(request):
    bad_request = HttpResponseBadRequest(status=400, content_type='application/json', content=json.dumps({'error_code': 1, 'error_message': 'Bad request'}))
    
    if request.method != 'POST':
        return bad_request
    
    body_json = json.loads(request.body)
    
    if not body_json.get('hostname', False) or not body_json.get('key', False) or not body_json['key'] == settings.SSH_HOST_CONFIGURATION_SECRET:
        return bad_request

    hostname = body_json['hostname']
    
    try:
        host_obj = Host.objects.get(hostname=hostname.upper())
        if body_json.get('hostkey', False) is False or body_json['hostkey'] != host_obj.key:
            return HttpResponseBadRequest(status=400, content_type='application/json', content=json.dumps({'error_code': 2, 'error_message': 'Host already exists, and cannot be bootstrapped again. Please provide the assigned guid for retrieving host configuration.'}))
        
    except Host.DoesNotExist:
        Host(hostname=hostname).save()
        
    finally:
        host_obj = Host.objects.get(hostname=hostname.upper())
        response = {
            'success': True,
            'hostname': host_obj.hostname,
            'hostkey': host_obj.key
        }
 
    return HttpResponse(status=201, content_type='application/json', content=json.dumps(response))

# Create your views here.
@csrf_exempt
def get_certificate(request):
    try:
        host_key_valid = Host.objects.get(key=request.headers.get('HOST-KEY', False))
    except Host.DoesNotExist:
        return HttpResponseBadRequest(status=400, content_type='text/plain', content='No host key provided or host key is invalid')
    
    
    with open(f"{settings.SSH_CA_CERT_PATH}.pub", 'r') as f:
        cert = f.read()
    
    if "PRIVATE KEY" not in cert:
        return HttpResponse(status=200, content_type='text/plain', content=cert)
    else:
        return HttpResponseBadRequest(status=400, content_type='text/plain', content="The server has been misconfigured. The request has been cancelled.")

# Principals are:
# Server name
# Hostgroup names the server belongs to
@csrf_exempt
def get_principals(request, servername):
    try:
        host = Host.objects.get(hostname=servername, key=request.headers.get('HOST-KEY', False))
    except Host.DoesNotExist:
        try:
            host = Host.objects.get(hostname=servername.upper(), key=request.headers.get('HOST-KEY', False))
        except Host.DoesNotExist:
            return HttpResponseBadRequest(status=400, content_type='text/plain', content="This server is not configured to be handled via this CA, or the host key is invalid. Please ask your administrator to add it.")

    host_groups = HostGroupAssignment.objects.filter(host=host.id)
    user_groups = GroupHostPermission.objects.filter(host=host.id)
    principals = [host.hostname]
    
    for item in host_groups:
        principals.append(f'hgr-{item.group.group_slug}')
    
    for item in user_groups:
        principals.append(f'ugr-{item.group.name}'.replace(' ', '-'))
        
    return HttpResponse(status=200, content_type='text/plain', content="\n".join(principals))