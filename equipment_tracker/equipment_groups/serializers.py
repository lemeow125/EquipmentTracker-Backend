from rest_framework import serializers
from .models import EquipmentGroup, EquipmentInstance
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes

# -- Equipment Group Serializers


class EquipmentGroupSerializer(serializers.HyperlinkedModelSerializer):
    date_added = serializers.DateTimeField(
        format="%m-%d-%Y %I:%M%p", read_only=True)
    last_updated = serializers.DateTimeField(
        format="%m-%d-%Y %I:%M%p", read_only=True)
    equipments = serializers.SlugRelatedField(
        many=True, slug_field='id', queryset=EquipmentInstance.objects.all())
    name = serializers.CharField()
    remarks = serializers.CharField()

    class Meta:
        model = EquipmentGroup
        fields = ('__all__')
        read_only_fields = ('id', 'last_updated', 'equipments',
                            'last_updated_by', 'date_added')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['equipments'] = [
            equipment.equipment.name for equipment in instance.equipments.all()]
        return representation
