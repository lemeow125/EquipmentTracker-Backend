# Generated by Django 4.2.7 on 2023-12-02 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('equipments', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipment',
            name='description',
            field=models.TextField(max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='equipmentinstance',
            name='remarks',
            field=models.TextField(max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='historicalequipment',
            name='description',
            field=models.TextField(max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='historicalequipmentinstance',
            name='remarks',
            field=models.TextField(max_length=512, null=True),
        ),
    ]
