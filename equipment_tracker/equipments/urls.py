from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
# For viewing all equipments
router.register(r'equipments', views.EquipmentViewSet)
router.register(r'equipment_instances', views.EquipmentInstanceViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    # Logs for all equipments
    path('equipments/logs', views.EquipmentsLogsViewSet.as_view()),
    # Logs for each equipment
    path('equipments/<int:equipment_id>/logs/',
         views.EquipmentLogViewSet.as_view({'get': 'list'})),
    # Last changed equipment
    path('equipments/latest', views.LastUpdatedEquipmentViewSet.as_view()),
    # Logs for all equipment instances
    path('equipment_instances/logs', views.EquipmentInstancesLogsViewSet.as_view()),
    # Logs for each equipment instance
    path('equipment_instances/<int:equipment_id>/logs/',
         views.EquipmentInstanceLogViewSet.as_view({'get': 'list'})),
    # Last changed equipment instance
    path('equipment_instances/latest',
         views.LastUpdatedEquipmentInstanceViewSet.as_view())
]
