# Generated by Django 5.0 on 2024-02-10 14:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apart', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='apart',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='aparts', to='apart.apartcategory'),
        ),
    ]
