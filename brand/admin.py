from django.contrib import admin
from .models import *


# Register your models here.

class BrandAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('brand_name',)
    }
    list_display = ('brand_name', 'slug')

    def has_view_permission(self, request, obj=None):
        return request.user.is_superadmin or request.user.is_admin or request.user.is_staff


admin.site.register(Brand, BrandAdmin)
