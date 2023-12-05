from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
# For viewing all equipments
router.register(r'equipment_groups', views.EquipmentGroupViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    # Logs for all equipments group
    path('equipment_groups/logs', views.EquipmentGroupsLogsViewSet.as_view()),
    # Logs for each equipment group
    path('equipment_groups/<int:group_id>/logs/',
         views.EquipmentGroupLogViewSet.as_view({'get': 'list'})),
    # Last changed equipment group
    path('equipment_groups/latest',
         views.LastUpdatedEquipmentGroupViewSet.as_view()),
]
