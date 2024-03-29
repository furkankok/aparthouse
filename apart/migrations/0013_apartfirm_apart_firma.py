# Generated by Django 5.0.2 on 2024-02-25 13:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apart', '0012_apartdistance_created_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApartFirm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('phone', models.CharField(blank=True, max_length=255, null=True)),
                ('mail', models.EmailField(blank=True, max_length=254, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='apart',
            name='firma',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='aparts', to='apart.apartfirm'),
        ),
    ]
