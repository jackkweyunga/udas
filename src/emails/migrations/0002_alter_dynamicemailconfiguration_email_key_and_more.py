# Generated by Django 4.0.3 on 2022-03-28 23:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emails', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dynamicemailconfiguration',
            name='email_key',
            field=models.CharField(default='nlhppqqk9DDq', max_length=1024),
        ),
        migrations.AlterField(
            model_name='dynamicemailconfiguration',
            name='name',
            field=models.CharField(default='ab4Fq2365EGj', max_length=256, verbose_name='email unique name'),
        ),
    ]
