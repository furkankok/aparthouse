# Generated by Django 5.0.2 on 2024-02-25 17:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apart', '0017_apartfirm_deleted_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apartuniversity',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='apart.city'),
        ),
    ]