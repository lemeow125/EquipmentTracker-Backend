from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, generics
from .models import EquipmentGroup
from . import serializers
from config.settings import DEBUG
from accounts.permissions import IsTechnician

# -- Equipment Viewsets


class EquipmentGroupViewSet(viewsets.ModelViewSet):
    if (not DEBUG):
        permission_classes = [IsAuthenticated, IsTechnician]
    serializer_class = serializers.EquipmentGroupSerializer
    queryset = EquipmentGroup.objects.all().order_by('id')

# For viewing all  logs for all equipments


class EquipmentGroupsLogsViewSet(generics.ListAPIView):
    if (not DEBUG):
        permission_classes = [IsAuthenticated, IsTechnician]
    serializer_class = serializers.EquipmentGroupLogsSerializer
    queryset = EquipmentGroup.history.all().order_by('-history_date')

# For viewing logs per individual equipment


class EquipmentGroupLogViewSet(viewsets.ReadOnlyModelViewSet):
    if (not DEBUG):
        permission_classes = [IsAuthenticated, IsTechnician]
    serializer_class = serializers.EquipmentGroupLogSerializer

    def get_queryset(self):
        group_id = self.kwargs['group_id']
        return EquipmentGroup.objects.filter(id=group_id)

# Last changed equipment


class LastUpdatedEquipmentGroupViewSet(generics.ListAPIView):
    if (not DEBUG):
        permission_classes = [IsAuthenticated, IsTechnician]
    serializer_class = serializers.EquipmentGroupSerializer
    queryset = EquipmentGroup.objects.all().order_by('-date_added')

    def get_queryset(self):
        return super().get_queryset()[:1]
