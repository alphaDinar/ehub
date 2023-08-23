# Generated by Django 4.2.1 on 2023-08-23 08:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Scheme', '0001_initial'),
        ('Log', '0001_initial'),
        ('Quiz', '0001_initial'),
        ('Course', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report', models.JSONField(blank=True, null=True)),
                ('student', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Log.student')),
            ],
        ),
        migrations.CreateModel(
            name='SchemeProgress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('progress_json', models.JSONField(blank=True, null=True)),
                ('progress_count', models.FloatField(default=0)),
                ('rating', models.IntegerField(default=0)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Course.course')),
                ('scheme', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Scheme.scheme')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Log.student')),
            ],
        ),
        migrations.CreateModel(
            name='QuizScore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('con', models.JSONField(blank=True, null=True)),
                ('ans_box', models.JSONField(blank=True, null=True)),
                ('mark', models.FloatField()),
                ('choice_box', models.JSONField(blank=True, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Course.course')),
                ('holder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Quiz.quiz')),
                ('scheme', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Scheme.scheme')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Log.student')),
            ],
        ),
        migrations.CreateModel(
            name='AssignmentScore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('con', models.JSONField(blank=True, null=True)),
                ('ans_box', models.JSONField(blank=True, null=True)),
                ('mark', models.FloatField()),
                ('choice_box', models.JSONField(blank=True, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Course.course')),
                ('holder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Quiz.assignment')),
                ('scheme', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Scheme.scheme')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Log.student')),
            ],
        ),
    ]