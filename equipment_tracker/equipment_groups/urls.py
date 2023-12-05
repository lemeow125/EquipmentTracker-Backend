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
    # Last changed equipment group
    path('equipment_groups/latest',
         views.LastUpdatedEquipmentGroupViewSet.as_view()),
]
