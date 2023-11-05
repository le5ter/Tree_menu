from django.contrib import admin
from .models import MenuItem


class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('text', 'menu_name', 'parent', 'url', 'named_url')
    list_filter = ('menu_name',)
    list_editable = ('url', 'named_url', 'parent')
    search_fields = ('text', 'menu_name')


admin.site.register(MenuItem, MenuItemAdmin)
