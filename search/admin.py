from django.contrib import admin

from search.models import SearchLog, FrequentSearch

# Register your models here.

class FrequentSearchAdmin(admin.ModelAdmin):
    list_display = ('search_term',)

admin.site.register(SearchLog)
admin.site.register(FrequentSearch,FrequentSearchAdmin)
