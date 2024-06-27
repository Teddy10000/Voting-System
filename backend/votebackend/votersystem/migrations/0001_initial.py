# Generated by Django 5.0.6 on 2024-06-27 19:39

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('department', models.ManyToManyField(to='votersystem.department')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_id', models.CharField(max_length=20, unique=True)),
                ('level', models.CharField(max_length=20)),
                ('age', models.PositiveIntegerField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='votersystem.course')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='votersystem.department')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Election',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('status', models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive')], max_length=10)),
                ('election_type', models.CharField(choices=[('General', 'General'), ('Departmental', 'Departmental'), ('Course', 'Course')], max_length=20)),
                ('course', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='votersystem.course')),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='votersystem.department')),
                ('managed_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='votersystem.student')),
            ],
        ),
        migrations.CreateModel(
            name='Candidate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_of_votes', models.PositiveIntegerField(default=0)),
                ('election', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='votersystem.election')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='votersystem.student')),
            ],
        ),
        migrations.CreateModel(
            name='Voter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='votersystem.student')),
            ],
        ),
        migrations.CreateModel(
            name='VoterRegistration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registered_on', models.DateTimeField(auto_now_add=True)),
                ('election', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='votersystem.election')),
                ('voter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='votersystem.voter')),
            ],
            options={
                'unique_together': {('voter', 'election')},
            },
        ),
        migrations.AddField(
            model_name='voter',
            name='elections',
            field=models.ManyToManyField(through='votersystem.VoterRegistration', to='votersystem.election'),
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cast_on', models.DateTimeField(auto_now_add=True)),
                ('candidate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='votersystem.candidate')),
                ('election', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='votersystem.election')),
                ('voter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='votersystem.voter')),
            ],
            options={
                'unique_together': {('voter', 'election')},
            },
        ),
    ]