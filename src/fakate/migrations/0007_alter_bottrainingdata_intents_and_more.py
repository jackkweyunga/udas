# Generated by Django 4.0.3 on 2022-04-16 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fakate', '0006_alter_bottrainingdata_intents_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bottrainingdata',
            name='intents',
            field=models.JSONField(default={'Intents': {'daktari': {'Answers': ['Aina gani ya daktari. \n', '1. Binafsi \n', '2. Umma'], 'Questions': ['Daktari']}, 'salamu': {'Answers': ['Karibu Fukate'], 'Questions': ['Habari', 'Hi']}, 'shukrani': {'Answers': ['Karibu tena.'], 'Questions': ['Asante']}}, 'Options': {'daktari': {'1': ['daktari binafsi'], '2': ['daktari wa umma']}}}),
        ),
        migrations.AlterField(
            model_name='bottrainingdata',
            name='labels',
            field=models.JSONField(default={'0': 'salamu', '1': 'shukrani', '2': 'daktari'}),
        ),
    ]
