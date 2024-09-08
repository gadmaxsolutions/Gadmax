from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.core.exceptions import PermissionDenied
from django.utils.html import format_html
from .models import *


# Register your models here.
class AccountAdmin(UserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'last_login', 'date_joined', 'is_active')
    list_display_links = ('username', 'first_name', 'last_name')
    readonly_fields = ('last_login', 'date_joined')
    ordering = ('-date_joined',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'mobile_number')}),
        ('Permissions', {'fields': ('is_admin', 'is_staff', 'is_active', 'is_superadmin')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superadmin:
            return self.readonly_fields + ('password',)
        return self.readonly_fields

    def get_fieldsets(self, request, obj=None):
        if not request.user.is_superadmin:
            # Remove or disable the password field for non-superusers
            fieldsets = super().get_fieldsets(request, obj)
            for fieldset in fieldsets:
                if 'password' in fieldset[1]['fields']:
                    fieldset[1]['fields'] = tuple(f for f in fieldset[1]['fields'] if f != 'password')
            return fieldsets
        return super().get_fieldsets(request, obj)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs

    def has_add_permission(self, request):
        return request.user.is_superadmin or request.user.is_admin

    def save_model(self, request, obj, form, change):
        # Prevent non-superadmins from setting is_superadmin=True
        if not request.user.is_superadmin and 'is_superadmin' in form.changed_data:
            if obj.is_superadmin:
                return False
                # raise PermissionDenied("You do not have permission to assign superadmin status.")
        super().save_model(request, obj, form, change)

    def has_change_permission(self, request, obj=None):
        if obj and obj.is_superadmin and not request.user.is_superadmin:
            return False
        return request.user.is_superadmin or request.user.is_admin

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superadmin

    def has_view_permission(self, request, obj=None):
        return request.user.is_superadmin or request.user.is_admin




class UserProfileAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        if object.profile_picture:
            return format_html(
                '<img src="{}" width="30" style="border-radius:50%;">'.format(object.profile_picture.url))
        else:
            return format_html('<img src="{}" width="30" style="border-radius:50%;">'.format(
                '/static/img/blank_profile.png'))  # Or simply return an empty string
    thumbnail.short_description='Profile Picture'
    list_display = ('thumbnail','user','city','district','state','country')

admin.site.register(Account, AccountAdmin)
admin.site.register(UserProfile, UserProfileAdmin)


admin.site.site_header = "GadMax"
admin.site.site_title = "GadMax"
admin.site.index_title = "Admin Panel"
