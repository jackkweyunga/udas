# Generated by Django 3.2.8 on 2021-10-14 16:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_dynamicemailconfiguration'),
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_id', models.CharField(max_length=25, unique=True)),
                ('service_key', models.UUIDField(default=uuid.UUID('cd87bd77-295b-489d-bcef-9d92f2eec3ee'))),
            ],
        ),
        migrations.CreateModel(
            name='ServicePackage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('price', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='ServiceUserSubscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='package_users', to='users.servicepackage', verbose_name='package')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscriptions', to=settings.AUTH_USER_MODEL, verbose_name='subscriber')),
            ],
        ),
        migrations.CreateModel(
            name='ServiceUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='services', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
        ),
        migrations.CreateModel(
            name='PackageFeatures',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feature', models.TextField()),
                ('package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='features', to='users.servicepackage', verbose_name='package')),
            ],
        ),
    ]
