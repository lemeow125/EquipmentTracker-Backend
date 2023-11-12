from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, generics
from .models import Equipment, EquipmentInstance
from . import serializers
from config.settings import DEBUG

# -- Equipment Viewsets


class EquipmentViewSet(viewsets.ModelViewSet):
    if (not DEBUG):
        permission_classes = [IsAuthenticated]
    serializer_class = serializers.EquipmentSerializer
    queryset = Equipment.objects.all().order_by('-date_added')

# For viewing all  logs for all equipments


class EquipmentsLogsViewSet(generics.ListAPIView):
    if (not DEBUG):
        permission_classes = [IsAuthenticated]
    serializer_class = serializers.EquipmentLogsSerializer
    queryset = Equipment.history.all().order_by('-history_date')

# For viewing logs per individual equipment


class EquipmentLogViewSet(viewsets.ReadOnlyModelViewSet):
    if (not DEBUG):
        permission_classes = [IsAuthenticated]
    serializer_class = serializers.EquipmentLogSerializer

    def get_queryset(self):
        equipment_id = self.kwargs['equipment_id']
        return Equipment.objects.filter(id=equipment_id)

# Last changed equipment


class LastUpdatedEquipmentViewSet(generics.ListAPIView):
    if (not DEBUG):
        permission_classes = [IsAuthenticated]
    serializer_class = serializers.EquipmentSerializer
    queryset = Equipment.objects.all().order_by('-date_added')

    def get_queryset(self):
        return super().get_queryset()[:1]

# -- Equipment Instance Viewsets


class EquipmentInstanceViewSet(viewsets.ModelViewSet):
    if (not DEBUG):
        permission_classes = [IsAuthenticated]
    serializer_class = serializers.EquipmentInstanceSerializer
    queryset = EquipmentInstance.objects.all().order_by('-date_added')

# For viewing all equipment instance logs


class EquipmentInstancesLogsViewSet(generics.ListAPIView):
    if (not DEBUG):
        permission_classes = [IsAuthenticated]
    serializer_class = serializers.EquipmentInstanceLogsSerializer
    queryset = EquipmentInstance.history.all().order_by('-history_date')

# For viewing logs per individual equipment instance


class EquipmentInstanceLogViewSet(viewsets.ReadOnlyModelViewSet):
    if (not DEBUG):
        permission_classes = [IsAuthenticated]
    serializer_class = serializers.EquipmentInstanceLogSerializer

    def get_queryset(self):
        equipment_id = self.kwargs['equipment_id']
        return EquipmentInstance.objects.filter(id=equipment_id)

# Last changed equipment instance


class LastUpdatedEquipmentInstanceViewSet(generics.ListAPIView):
    if (not DEBUG):
        permission_classes = [IsAuthenticated]
    serializer_class = serializers.EquipmentInstanceSerializer
    queryset = EquipmentInstance.objects.all().order_by('-date_added')

    def get_queryset(self):
        return super().get_queryset()[:1]
