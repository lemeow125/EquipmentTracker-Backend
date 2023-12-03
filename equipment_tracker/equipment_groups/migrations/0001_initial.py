# Generated by Django 4.2.7 on 2023-12-02 12:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import simple_history.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('equipments', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalEquipmentGroup',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('remarks', models.TextField(max_length=512)),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('last_updated', models.DateTimeField(blank=True, editable=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical equipment group',
                'verbose_name_plural': 'historical equipment groups',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='EquipmentGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('remarks', models.TextField(max_length=512)),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('equipments', models.ManyToManyField(to='equipments.equipmentinstance')),
            ],
        ),
    ]
