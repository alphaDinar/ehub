# Generated by Django 4.2.1 on 2023-08-23 09:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Course', '0001_initial'),
        ('SuperManager', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TimeTableTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='default timetable template', max_length=200)),
                ('headers', models.JSONField(default=list)),
                ('con', models.JSONField(default=list)),
            ],
        ),
        migrations.CreateModel(
            name='TimeTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('headers', models.JSONField(default=list)),
                ('con', models.JSONField(default=list)),
                ('grade', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Course.grade')),
            ],
        ),
    ]
