from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseBadRequest
from django.conf import settings
from .models import Host, HostGroupAssignment


# Create your views here.
@csrf_exempt
def get_certificate(request):
    with open("%s.pub" % settings.SSH_CA_CERT_PATH, 'r') as f:
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
        host = Host.objects.get(hostname=servername)
    except Host.DoesNotExist:
        try:
            host = Host.objects.get(hostname=servername.upper())
        except Host.DoesNotExist:
            return HttpResponseBadRequest(status=400, content_type='text/plain', content="This server is not configured to be handled via this CA. Please ask your administrator to add it.")

    hostgroups = HostGroupAssignment.objects.filter(host=host.id)

    principals = [host.hostname]
    for item in hostgroups:
        principals.append(item.group.group_slug)
        
    return HttpResponse(status=200, content_type='text/plain', content="\n".join(principals))