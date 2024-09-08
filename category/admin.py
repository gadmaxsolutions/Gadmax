from django.contrib import admin
from .models import *


# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('category_name',)
    }
    list_display = ('category_name', 'slug')

    def has_view_permission(self, request, obj=None):
        return request.user.is_superadmin or request.user.is_admin or request.user.is_staff



admin.site.register(Category, CategoryAdmin)


class MainCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('category_name',)
    }
    list_display = ('category_name', 'slug')

    def has_view_permission(self, request, obj=None):
        return request.user.is_superadmin or request.user.is_admin or request.user.is_staff

admin.site.register(MainCategory, MainCategoryAdmin)
