# Generated by Django 5.1.5 on 2025-02-09 16:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0006_alter_lease_property_alter_lease_tenant'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='lease',
            name='tenant',
            field=models.OneToOneField(limit_choices_to={'role': 'Tenant'}, on_delete=django.db.models.deletion.CASCADE, related_name='lease', to=settings.AUTH_USER_MODEL),
        ),
    ]
