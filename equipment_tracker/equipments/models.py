from django.db import models
from django.utils.timezone import now
from simple_history.models import HistoricalRecords
from django.db.models.signals import post_migrate
from django.dispatch import receiver
# Create your models here.


class Equipment(models.Model):
    name = models.CharField(max_length=40)
    description = models.TextField(max_length=512)
    date_added = models.DateTimeField(default=now, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    history = HistoricalRecords()

    def __str__(self):
        return f'{self.name} ID:{self.id}'


class EquipmentInstance(models.Model):
    STATUS_CHOICES = (
        ('Working', 'Working'),
        ('Broken', 'Broken'),
        ('Under Maintenance', 'Under Maintenance'),
        ('Decomissioned', 'Decomissioned  '),
    )

    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='PENDING')
    remarks = models.TextField(max_length=512)
    date_added = models.DateTimeField(default=now, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    history = HistoricalRecords()

    def __str__(self):
        return f'{self.equipment.name} ID:{self.id}'


@receiver(post_migrate)
def create_superuser(sender, **kwargs):
    if sender.name == 'equipments':
        EQUIPMENT, CREATED = Equipment.objects.get_or_create(
            name="HP All-in-One PC", description="I5 6500 8GB RAM 1TB HDD")
        EQUIPMENT_INSTANCE, CREATED = EquipmentInstance.objects.get_or_create(
            equipment=EQUIPMENT, status="Working", remarks="First PC of citc equipment tracker!")
        EQUIPMENT, CREATED = Equipment.objects.get_or_create(
            name="HP Keyboard", description="Generic Membrane Keyboard")
        EQUIPMENT_INSTANCE, CREATED = EquipmentInstance.objects.get_or_create(
            equipment=EQUIPMENT, status="Working", remarks="First keyboard of citc equipment tracker!")
        EQUIPMENT, CREATED = Equipment.objects.get_or_create(
            name="HP Mouse", description="Generic Mouse")
        EQUIPMENT_INSTANCE, CREATED = EquipmentInstance.objects.get_or_create(
            equipment=EQUIPMENT, status="Working", remarks="First mouse of citc equipment tracker!")
