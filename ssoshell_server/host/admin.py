from django.contrib import admin

from .models import Host, HostGroup, HostGroupAssignment, UserHostgroupPermission, GroupHostgroupPermission, UserHostPermission, GroupHostPermission

class HostGroupAssignmentInline(admin.TabularInline):
    model = HostGroupAssignment
    extra = 0
    
class UserHostgroupPermissionAdmin(admin.TabularInline):
    model = UserHostgroupPermission
    extra = 0
    
class GroupHostgroupPermissionAdmin(admin.TabularInline):
    model = GroupHostgroupPermission
    extra = 0

class UserHostPermissionAdmin(admin.TabularInline):
    model = UserHostPermission
    extra = 0
    
class GroupHostPermissionAdmin(admin.TabularInline):
    model = GroupHostPermission
    extra = 0

class HostsAdmin(admin.ModelAdmin):
    
    fieldsets = [
        ("Enter the hostname for the server", {'fields': ['hostname']}),
    ]
    list_display = ['hostname']
    inlines = [HostGroupAssignmentInline, UserHostPermissionAdmin, GroupHostPermissionAdmin]

class HostGroupsAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Enter a name for your host group', {'fields': ['groupname']}),
        ('Enter a slug for your group name (Only a-zA-Z0-9)', {'fields': ['group_slug']}),
    ]
    list_display = ['groupname', 'group_slug']
    inlines = [HostGroupAssignmentInline, UserHostgroupPermissionAdmin, GroupHostgroupPermissionAdmin]
    

admin.site.register(Host, HostsAdmin)
admin.site.register(HostGroup, HostGroupsAdmin)