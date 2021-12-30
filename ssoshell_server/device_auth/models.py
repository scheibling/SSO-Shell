from django.db import models

class AuthRequest(models.Model):
    token = models.CharField(primary_key=True, max_length=20, unique=True)
    public_key = models.TextField(null=False, blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    
class AuthCompleted(models.Model):
    serial = models.IntegerField(primary_key=True, null=False, blank=False, unique=True, auto_created=True)
    token = models.CharField(max_length=20, null=False, blank=False, unique=True)
    user_id = models.IntegerField(null=False, blank=False, unique=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    certificate_subject = models.CharField(max_length=255, null=False, blank=False)
    certificate_principals = models.TextField(null=False, blank=True)
    signed_key = models.TextField(null=False, blank=False, default="None")