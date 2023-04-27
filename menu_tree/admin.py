from django.contrib import admin

from menu_tree.models import Menu, MenuRelation, MenuItem


admin.site.register(Menu)
admin.site.register(MenuRelation)
admin.site.register(MenuItem)
