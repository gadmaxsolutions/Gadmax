from django.contrib import admin
from .models import *
import admin_thumbnails


# Register your models here.
@admin_thumbnails.thumbnail('image')
class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'category', 'modified_date', 'is_available')
    prepopulated_fields = {
        'slug': ('product_name',)
    }
    inlines = [ProductGalleryInline]

    def has_view_permission(self, request, obj=None):
        return request.user.is_superadmin or request.user.is_admin or request.user.is_staff


admin.site.register(Products,ProductAdmin)

class VariationAdmin(admin.ModelAdmin):
    list_display = ('product','variation_category','variation_value','is_active')
    list_editable = ('is_active',)
    list_filter = ('product','variation_category','variation_value','is_active')

    def has_view_permission(self, request, obj=None):
        return request.user.is_superadmin or request.user.is_admin or request.user.is_staff
admin.site.register(Variation,VariationAdmin)


admin.site.register(ProductGallery)
admin.site.register(ReviewRating)
