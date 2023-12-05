from django.urls import path, include

urlpatterns = [
    path('accounts/', include('accounts.urls')),
    path('equipments/', include('equipments.urls')),
    path('equipment_groups/', include('equipment_groups.urls'))
]
