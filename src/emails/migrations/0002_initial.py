# Generated by Django 4.0.3 on 2022-03-26 10:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('emails', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dynamicemailconfiguration',
            name='created_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='emails', to=settings.AUTH_USER_MODEL, verbose_name='creator'),
        ),
    ]