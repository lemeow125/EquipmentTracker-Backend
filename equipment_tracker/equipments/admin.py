from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Equipment, EquipmentInstance


@admin.register(Equipment)
class EquipmentAdmin(SimpleHistoryAdmin):
    readonly_fields = ('date_added', 'last_updated')
    list_display = ('name', 'date_added', 'last_updated')


@admin.register(EquipmentInstance)
class EquipmentInstanceAdmin(SimpleHistoryAdmin):
    readonly_fields = ('date_added', 'last_updated')
    list_display = ('equipment', 'status', 'remarks',
                    'date_added', 'last_updated')
