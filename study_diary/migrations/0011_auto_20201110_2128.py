# Generated by Django 3.1.2 on 2020-11-10 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('study_diary', '0010_auto_20201108_1518'),
    ]

    operations = [
        migrations.AlterField(
            model_name='daily',
            name='category',
            field=models.CharField(default=None, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='daily',
            name='check',
            field=models.IntegerField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='daily',
            name='content',
            field=models.CharField(default=None, max_length=50, null=True),
        ),
    ]