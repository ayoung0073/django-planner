# Generated by Django 3.1.2 on 2020-11-07 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('study_diary', '0004_auto_20201107_1819'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diary',
            name='date',
            field=models.DateField(),
        ),
    ]
