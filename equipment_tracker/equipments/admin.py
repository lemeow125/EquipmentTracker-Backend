from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Equipment, EquipmentInstance

admin.site.register(Equipment, SimpleHistoryAdmin)
admin.site.register(EquipmentInstance, SimpleHistoryAdmin)
