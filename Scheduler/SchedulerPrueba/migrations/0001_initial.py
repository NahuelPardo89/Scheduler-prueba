# Generated by Django 4.1.7 on 2023-03-27 17:20

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('schedule', '0014_use_autofields_for_pk'),
    ]

    operations = [
        migrations.CreateModel(
            name='Medico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dni', models.IntegerField(unique=True)),
                ('nombre', models.CharField(max_length=100)),
                ('especialidad', models.CharField(max_length=100)),
                ('calendario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='schedule.calendar')),
            ],
        ),
        migrations.CreateModel(
            name='Paciente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('telefono', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Turno',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('hora', models.TimeField()),
                ('recurrente', models.BooleanField()),
                ('duracion', models.DurationField(default=datetime.timedelta(seconds=3600))),
                ('estado', models.CharField(choices=[('P', 'Pendiente'), ('C', 'Confirmado'), ('A', 'Atendido'), ('F', 'Finalizado')], default='P', max_length=1)),
                ('evento', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='schedule.event')),
                ('medico', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SchedulerPrueba.medico')),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SchedulerPrueba.paciente')),
            ],
        ),
        migrations.CreateModel(
            name='HorarioMedico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dia_semana', models.IntegerField(choices=[(0, 'Lunes'), (1, 'Martes'), (2, 'Miércoles'), (3, 'Jueves'), (4, 'Viernes'), (5, 'Sábado'), (6, 'Domingo')])),
                ('hora_inicio', models.TimeField()),
                ('hora_fin', models.TimeField()),
                ('medico', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='horarios', to='SchedulerPrueba.medico')),
            ],
            options={
                'verbose_name_plural': 'Horarios Médicos',
                'unique_together': {('medico', 'dia_semana', 'hora_inicio', 'hora_fin')},
            },
        ),
    ]
