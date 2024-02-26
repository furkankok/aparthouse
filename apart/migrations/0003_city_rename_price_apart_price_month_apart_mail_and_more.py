# Generated by Django 5.0 on 2024-02-12 03:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apart', '0002_apart_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('country', models.CharField(blank=True, default='Türkiye', max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.RenameField(
            model_name='apart',
            old_name='price',
            new_name='price_month',
        ),
        migrations.AddField(
            model_name='apart',
            name='mail',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='apart',
            name='price_season',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='apart',
            name='price_year',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='Town',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='towns', to='apart.city')),
            ],
        ),
        migrations.AddField(
            model_name='apart',
            name='town',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='aparts', to='apart.town'),
        ),
    ]
