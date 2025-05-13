from django.db import models
from django.contrib import admin

from .models import Menu, MenuItem


class MenuItemInline(admin.StackedInline):
    model = MenuItem
    extra = 1

    def save_new_objects(self, commit=True):
        """
        Вставка order внутри инлайнов.
        """
        objs = super().save_new_objects(commit=False)
        for obj in objs:
            if obj.order == 0:
                siblings = MenuItem.objects.filter(menu=obj.menu, parent=obj.parent)
                max_order = siblings.aggregate(models.Max('order'))['order__max'] or 0
                obj.order = max_order + 10
        if commit:
            for obj in objs:
                obj.save()
        return objs


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    inlines = [MenuItemInline]


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'menu', 'parent', 'order')

    def save_model(self, request, obj, form, change):
        if not obj.order:
            siblings = MenuItem.objects.filter(menu=obj.menu, parent=obj.parent)
            max_order = siblings.aggregate(models.Max('order'))['order__max'] or 0
            obj.order = max_order + 10
        super().save_model(request, obj, form, change)
