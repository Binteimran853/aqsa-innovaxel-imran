from django.contrib import admin
from .models import URL

@admin.register(URL)
class URLAdmin(admin.ModelAdmin):
    list_display = ['url', 'shortCode', 'accessCount', 'createdAt', 'updatedAt']
    search_fields = ['url', 'shortCode']
    list_filter = ['createdAt', 'updatedAt']
