from django.db import models
from django.utils.timezone import now
from simple_history.models import HistoricalRecords
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from equipments.models import EquipmentInstance


class EquipmentGroup(models.Model):
    name = models.CharField(max_length=200)
    remarks = models.TextField(max_length=512)
    date_added = models.DateTimeField(default=now, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    equipments = models.ManyToManyField(EquipmentInstance)
    history = HistoricalRecords()

    @property
    def status(self):
        if self.equipments.filter(status='Broken').exists():
            return 'Broken'
        elif self.equipments.filter(status='Under Maintenance').exists():
            return 'Under Maintenance'
        elif self.equipments.filter(status='Decomissioned').exists():
            return 'Decomissioned'
        else:
            return 'Working'

    def __str__(self):
        return self.name


@receiver(post_migrate)
def create_superuser(sender, **kwargs):
    if sender.name == 'equipment_groups':
        PC = EquipmentInstance.objects.filter(id=1).first().id
        KEYBOARD = EquipmentInstance.objects.filter(id=2).first().id
        MOUSE = EquipmentInstance.objects.filter(id=3).first().id
        GROUP, CREATED = EquipmentGroup.objects.get_or_create(
            name="HP All-In-One PC Set", remarks="First PC set of citc tracker!")
        GROUP.equipments.set([PC, KEYBOARD, MOUSE])
