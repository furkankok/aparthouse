# Generated by Django 5.0.2 on 2024-02-23 02:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apart', '0008_apart_created_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='RightsSupport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'permissions': (('yonetici', 'Yönetici'),),
                'managed': False,
                'default_permissions': (),
            },
        ),
    ]
