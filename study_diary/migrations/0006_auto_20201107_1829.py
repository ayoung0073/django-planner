# Generated by Django 3.1.2 on 2020-11-07 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('study_diary', '0005_auto_20201107_1827'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diary',
            name='date',
            field=models.CharField(max_length=10),
        ),
    ]