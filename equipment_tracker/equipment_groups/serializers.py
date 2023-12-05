from rest_framework import serializers
from .models import EquipmentGroup
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes

# -- Equipment Group Serializers


class EquipmentGroupHistoricalRecordField(serializers.ListField):
    child = serializers.DictField()

    def to_representation(self, data):
        return super().to_representation(data.values('name', 'remarks', 'history_date', 'history_user').order_by('-history_date'))


class EquipmentGroupSerializer(serializers.HyperlinkedModelSerializer):
    date_added = serializers.DateTimeField(
        format="%m-%d-%Y %I:%M%p", read_only=True)
    last_updated = serializers.DateTimeField(
        format="%m-%d-%Y %I:%M%p", read_only=True)
    last_updated_by = serializers.SerializerMethodField()
    name = serializers.CharField()
    remarks = serializers.CharField()

    class Meta:
        model = EquipmentGroup
        fields = ('id', 'name', 'remarks',
                  'last_updated', 'last_updated_by', 'date_added')
        read_only_fields = ('id', 'last_updated',
                            'last_updated_by', 'date_added')

    @extend_schema_field(OpenApiTypes.STR)
    def get_history_user(self, obj):
        return obj.history_user.username if obj.history_user else None

    @extend_schema_field(OpenApiTypes.STR)
    def get_last_updated_by(self, obj):
        return obj.history.first().history_user.username if obj.history.first().history_user else None


class EquipmentGroupLogsSerializer(serializers.HyperlinkedModelSerializer):
    history_date = serializers.DateTimeField(
        format="%m-%d-%Y %I:%M%p", read_only=True)
    history_user = serializers.SerializerMethodField()

    class Meta:
        model = EquipmentGroup.history.model
        fields = ('history_id', 'id', 'name', 'remarks',
                  'history_date', 'history_user')
        read_only_fields = ('history_id', 'id', 'name', 'remarks',
                            'history_date', 'history_user')

    @extend_schema_field(OpenApiTypes.STR)
    def get_history_user(self, obj):
        return obj.history_user.username if obj.history_user else None


class EquipmentGroupLogSerializer(serializers.HyperlinkedModelSerializer):
    date_added = serializers.DateTimeField(
        format="%m-%d-%Y %I:%M%p", read_only=True)
    last_updated = serializers.DateTimeField(
        format="%m-%d-%Y %I:%M%p", read_only=True)
    last_updated_by = serializers.SerializerMethodField()
    name = serializers.CharField()
    remarks = serializers.CharField(required=False)
    history = EquipmentGroupHistoricalRecordField()

    class Meta:
        model = EquipmentGroup
        fields = ('id', 'name', 'remarks',
                  'last_updated', 'date_added', 'last_updated_by', 'history')
        read_only_fields = ('id', 'last_updated',
                            'date_added', 'last_updated_by', 'history')

    @extend_schema_field(OpenApiTypes.STR)
    def get_last_updated_by(self, obj):
        return obj.history.first().history_user.username if obj.history.first().history_user else None
