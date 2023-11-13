from django.contrib import admin
from .models import EquipmentGroup
from simple_history.admin import SimpleHistoryAdmin


@admin.register(EquipmentGroup)
class EquipmentGroupAdmin(SimpleHistoryAdmin):
    readonly_fields = ['status']
    list_display = ('name', 'status', 'date_added', 'last_updated')
