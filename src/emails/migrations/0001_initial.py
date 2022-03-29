# Generated by Django 4.0.3 on 2022-03-28 23:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DynamicEmailConfiguration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='F8a9iHApdcGb', max_length=256, verbose_name='email unique name')),
                ('slug', models.SlugField(default='djangodbmodelsfieldscharfield', unique=True, verbose_name='slug')),
                ('email_key', models.CharField(default='nC645qIaFfah', max_length=1024)),
                ('host', models.CharField(blank=True, default='smtp.gmail.com', max_length=256, null=True, verbose_name='Email Host')),
                ('port', models.SmallIntegerField(blank=True, default=587, null=True, verbose_name='Email Port')),
                ('email_name', models.CharField(blank=True, max_length=256, null=True, verbose_name='Default From Email')),
                ('username', models.CharField(blank=True, max_length=256, null=True, verbose_name='Email Authentication Username')),
                ('password', models.CharField(blank=True, max_length=256, null=True, verbose_name='Email Authentication Password')),
                ('use_tls', models.BooleanField(default=True, verbose_name='Use TLS')),
                ('use_ssl', models.BooleanField(default=False, verbose_name='Use SSL')),
                ('fail_silently', models.BooleanField(default=False, verbose_name='Fail Silently')),
                ('timeout', models.SmallIntegerField(blank=True, null=True, verbose_name='Email Send Timeout (seconds)')),
                ('created_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='emails', to=settings.AUTH_USER_MODEL, verbose_name='creator')),
            ],
            options={
                'verbose_name': 'Email Configuration',
            },
        ),
    ]
