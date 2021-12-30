from django.db import models
from django.contrib.auth.models import User, Group

# Convert all hostnames to uppercase for storage
class UpperCaseCharField(models.CharField):
    def __init__(self, *args, **kwargs):
            super(UpperCaseCharField, self).__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        value = getattr(model_instance, self.attname, None)
        if value:
            value = value.upper()
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super(UpperCaseCharField, self).pre_save(model_instance, add)

# Create your models here.
class Host(models.Model):
    id = models.AutoField(primary_key=True)
    hostname = UpperCaseCharField(max_length=255)
    def __str__(self):
        return self.hostname

class HostGroup(models.Model):
    id = models.AutoField(primary_key=True)
    groupname = models.CharField(max_length=255)
    group_slug = models.CharField(max_length=255, blank=False, null=False, unique=True)
    def __str__(self):
        return self.groupname

class HostGroupAssignment(models.Model):
    id = models.AutoField(primary_key=True)
    host = models.ForeignKey(Host, on_delete=models.CASCADE)
    group = models.ForeignKey(HostGroup, on_delete=models.CASCADE)
    def __str__(self):
        return "{} is assigned to {}".format(self.host, self.group)
    

class UserHostPermission(models.Model):
    id = models.AutoField(primary_key=True)
    host = models.ForeignKey(Host, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return "User {} has permissions to {}".format(self.user, self.host)
    
class GroupHostPermission(models.Model):
    id = models.AutoField(primary_key=True)
    host = models.ForeignKey(Host, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    def __str__(self):
        return "Group {} has permissions to {}".format(self.group, self.host)
    
    
class UserHostgroupPermission(models.Model):
    id = models.AutoField(primary_key=True)
    hostgroup = models.ForeignKey(HostGroup, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return "User: {} has permission to hostgroup {}".format(self.user.username, self.hostgroup.groupname)
    
class GroupHostgroupPermission(models.Model):
    id = models.AutoField(primary_key=True)
    hostgroup = models.ForeignKey(HostGroup, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    def __str__(self):
        return "Users in group {} have permission to hostgroup {}".format(self.group.name, self.hostgroup.groupname)
    

    
