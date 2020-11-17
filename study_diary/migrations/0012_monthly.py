# Generated by Django 3.1.2 on 2020-11-16 16:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('study_diary', '0011_auto_20201110_2128'),
    ]

    operations = [
        migrations.CreateModel(
            name='Monthly',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('content', models.CharField(default=None, max_length=40, null=True)),
                ('writer', models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, to='study_diary.user')),
            ],
        ),
    ]