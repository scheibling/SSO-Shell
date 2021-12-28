from django.db import models


class AuthRequest(models.Model):
    user_id = models.IntegerField(null=False, blank=False)
    token = models.CharField(max_length=20, null=False, blank=False, unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    verified = models.BooleanField(default=False)
    
class CertificatesIssued(models.Model):
    serial_no = models.CharField(max_length=40, null=False, blank=False, primary_key=True, unique=True)
    subject = models.CharField(max_length=255, null=False, blank=False)
    permissions = models.CharField(max_length=255, null=False, blank=True)
    

