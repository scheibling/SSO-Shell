from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import os
import json
from pathlib import Path



# Create your views here.
def success(request):
    if request.session.get('redirect', False):
        return HttpResponseRedirect(request.session.get('redirect'))
    return HttpResponse('Success! You can now close this window and return to your application')