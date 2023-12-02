from rest_framework import serializers
from .models import Equipment, EquipmentInstance
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes
from django.db.models import F
from accounts.models import CustomUser

# -- Equipment Serializers


class EquipmentHistoricalRecordField(serializers.ListField):
    child = serializers.DictField()

    def to_representation(self, data):
        return super().to_representation(data.values('name', 'description', 'category', 'history_date', 'history_user').order_by('-history_date'))


class EquipmentSerializer(serializers.HyperlinkedModelSerializer):
    date_added = serializers.DateTimeField(
        format="%m-%d-%Y %I:%M%p", read_only=True)
    last_updated = serializers.DateTimeField(
        format="%m-%d-%Y %I:%M%p", read_only=True)
    last_updated_by = serializers.SerializerMethodField()
    name = serializers.CharField()
    description = serializers.CharField()

    class Meta:
        model = Equipment
        fields = ('id', 'name', 'description', 'category',
                  'last_updated', 'last_updated_by', 'date_added')
        read_only_fields = ('id', 'last_updated',
                            'last_updated_by', 'date_added')

    @extend_schema_field(OpenApiTypes.STR)
    def get_history_user(self, obj):
        return obj.history_user.username if obj.history_user else None

    @extend_schema_field(OpenApiTypes.STR)
    def get_last_updated_by(self, obj):
        return obj.history.first().history_user.username if obj.history.first().history_user else None


class EquipmentLogsSerializer(serializers.HyperlinkedModelSerializer):
    history_date = serializers.DateTimeField(
        format="%m-%d-%Y %I:%M%p", read_only=True)
    history_user = serializers.SerializerMethodField()

    class Meta:
        model = Equipment.history.model
        fields = ('history_id', 'name', 'description', 'category',
                  'history_date', 'history_user')
        read_only_fields = ('history_id', 'id', 'name', 'description',
                            'history_date', 'history_user')

    @extend_schema_field(OpenApiTypes.STR)
    def get_history_user(self, obj):
        return obj.history_user.username if obj.history_user else None


class EquipmentLogSerializer(serializers.HyperlinkedModelSerializer):
    date_added = serializers.DateTimeField(
        format="%m-%d-%Y %I:%M%p", read_only=True)
    last_updated = serializers.DateTimeField(
        format="%m-%d-%Y %I:%M%p", read_only=True)
    last_updated_by = serializers.SerializerMethodField()
    name = serializers.CharField()
    description = serializers.CharField()
    history = EquipmentHistoricalRecordField()

    class Meta:
        model = Equipment
        fields = ('id', 'name', 'description', 'category',
                  'last_updated', 'date_added', 'last_updated_by', 'history')
        read_only_fields = ('id', 'last_updated',
                            'date_added', 'last_updated_by', 'history')

    @extend_schema_field(OpenApiTypes.STR)
    def get_last_updated_by(self, obj):
        return obj.history.first().history_user.username if obj.history.first().history_user else None

# -- Equipment Instance Serializers


class EquipmentInstanceHistoricalRecordField(serializers.ListField):
    child = serializers.DictField()

    def to_representation(self, data):
        data = data.annotate(equipment_name=F('equipment__name'))
        return super().to_representation(data.values('equipment', 'equipment_name', 'status', 'remarks', 'history_date', 'history_user').order_by('-history_date'))


class EquipmentInstanceSerializer(serializers.HyperlinkedModelSerializer):
    equipment = serializers.SlugRelatedField(
        slug_field='id', queryset=Equipment.objects.all())
    equipment_name = serializers.CharField(
        source='equipment.name', read_only=True)
    status = serializers.CharField()
    remarks = serializers.CharField()
    date_added = serializers.DateTimeField(
        format="%m-%d-%Y %I:%M%p", read_only=True)
    last_updated = serializers.DateTimeField(
        format="%m-%d-%Y %I:%M%p", read_only=True)
    last_updated_by = serializers.SerializerMethodField()
    status = serializers.ChoiceField(choices=EquipmentInstance.STATUS_CHOICES)

    # Forbid user from changing equipment field once the instance is already created
    def update(self, instance, validated_data):
        # Ignore any changes to 'equipment'
        validated_data.pop('equipment', None)
        return super().update(instance, validated_data)

    class Meta:
        model = EquipmentInstance
        fields = ('id', 'equipment', 'equipment_name', 'status', 'remarks',
                  'last_updated', 'last_updated_by', 'date_added')
        read_only_fields = ('id', 'last_updated',
                            'last_updated_by', 'date_added', 'equipment_name')

    @extend_schema_field(OpenApiTypes.STR)
    def get_history_user(self, obj):
        return obj.history_user.username if obj.history_user else None

    @extend_schema_field(OpenApiTypes.STR)
    def get_last_updated_by(self, obj):
        return obj.history.first().history_user.username if obj.history.first().history_user else None


class EquipmentInstanceLogsSerializer(serializers.HyperlinkedModelSerializer):
    history_date = serializers.DateTimeField(
        format="%m-%d-%Y %I:%M%p", read_only=True)
    history_user = serializers.SerializerMethodField()
    equipment = serializers.SlugRelatedField(
        slug_field='id', queryset=Equipment.objects.all())
    equipment_name = serializers.CharField(
        source='equipment.name', read_only=True)

    class Meta:
        model = EquipmentInstance.history.model
        fields = ('history_id', 'id', 'equipment', 'equipment_name', 'status', 'remarks',
                  'history_date', 'history_user')
        read_only_fields = ('history_id', 'id', 'equipment', 'status', 'remarks',
                            'history_date', 'history_user', 'equipment_name')

    @extend_schema_field(OpenApiTypes.STR)
    def get_history_user(self, obj):
        return obj.history_user.username if obj.history_user else None


class EquipmentInstanceLogSerializer(serializers.HyperlinkedModelSerializer):
    equipment = serializers.SlugRelatedField(
        slug_field='id', queryset=Equipment.objects.all())
    equipment_name = serializers.CharField(
        source='equipment.name', read_only=True)
    status = serializers.CharField()
    remarks = serializers.CharField()
    date_added = serializers.DateTimeField(
        format="%m-%d-%Y %I:%M%p", read_only=True)
    last_updated = serializers.DateTimeField(
        format="%m-%d-%Y %I:%M%p", read_only=True)
    last_updated_by = serializers.SerializerMethodField()
    history = EquipmentInstanceHistoricalRecordField()

    # Forbid user from changing equipment field once the instance is already created
    def update(self, instance, validated_data):
        # Ignore any changes to 'equipment'
        validated_data.pop('equipment', None)
        return super().update(instance, validated_data)

    class Meta:
        model = EquipmentInstance
        fields = ('id', 'equipment', 'equipment_name', 'status', 'remarks',
                  'last_updated', 'date_added', 'last_updated_by', 'history')
        read_only_fields = ('id', 'last_updated',
                            'date_added', 'last_updated_by', 'history', 'equipment_name')

    @extend_schema_field(OpenApiTypes.STR)
    def get_last_updated_by(self, obj):
        return obj.history.first().history_user.username if obj.history.first().history_user else None
