from django.db import models
from django.urls import reverse

from django.utils import timezone
from django.conf import settings
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from datetime import datetime, time
from schedule.models import Calendar, Event, Rule


class Medico(models.Model):
    dni=models.IntegerField(unique=True)
    nombre = models.CharField(max_length=100)
    especialidad = models.CharField(max_length=100)
    calendario = models.ForeignKey(Calendar, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.nombre
    
    @staticmethod
    def crear_calendario(nombre,dni):
        dni=str(dni)
        slug = slugify(f"{nombre}{dni}")
        return Calendar.objects.create(
            name=f"calendario de {nombre}",
            slug=slug
        )
    @property
    def turnos(self):
        return Turno.objects.filter(medico=self)
    
    def save(self, *args, **kwargs):
        if not self.calendario:
            self.calendario = self.crear_calendario(self.nombre,self.dni)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.calendario.delete() # eliminar el calendario asociado
        super().delete(*args, **kwargs) # eliminar el objeto Medico

        
class HorarioMedico(models.Model):
    # Definimos las opciones para el campo dia_semana
    DIA_SEMANA_CHOICES = [
        (0, 'Lunes'),
        (1, 'Martes'),
        (2, 'Miércoles'),
        (3, 'Jueves'),
        (4, 'Viernes'),
        (5, 'Sábado'),
        (6, 'Domingo'),
    ]

    # Definimos la relación con el modelo Medico
    medico = models.ForeignKey('Medico', on_delete=models.CASCADE, related_name='horarios')

    # Definimos el día de la semana, con opciones predefinidas
    dia_semana = models.IntegerField(choices=DIA_SEMANA_CHOICES)

    # Definimos la hora de inicio del horario
    hora_inicio = models.TimeField()

    # Definimos la hora de fin del horario
    hora_fin = models.TimeField()

    class Meta:
        verbose_name_plural = 'Horarios Médicos'
        # Definimos la unicidad del horario para un medico en un dia/hora especificos
        unique_together = ('medico', 'dia_semana', 'hora_inicio', 'hora_fin')

    def __str__(self):
        # Devolvemos una cadena representando el horario
        return f"{self.medico} ({self.get_dia_semana_display()} {self.hora_inicio} - {self.hora_fin})"

    # Verifica si el horario se superpone con algún otro horario de la misma semana del mismo médico
    def horario_superpuesto(self):
        # Obtiene los horarios del mismo médico en el mismo día de la semana, excluyendo el horario actual
        horarios = HorarioMedico.objects.filter(
            medico=self.medico,
            dia_semana=self.dia_semana,
        ).exclude(pk=self.pk)

        # Compara los horarios para detectar si se superponen
        for horario in horarios:
            if self.hora_inicio < horario.hora_fin and self.hora_fin > horario.hora_inicio:
                return True

        return False

    @staticmethod
    def obtener_horario_medico(medico):
        # Devuelve los horarios para un medico
        return HorarioMedico.objects.filter(medico=medico)
        


class Paciente(models.Model):
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre

    def turnos(self):
        return Turno.objects.filter(paciente=self)

class Turno(models.Model):
    ESTADO_CHOICES = [
        ('P', 'Pendiente'),
        ('C', 'Confirmado'),
        ('A', 'Atendido'),
        ('F', 'Finalizado'),
    ]
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    fecha = models.DateField()  # fecha del turno
    hora = models.TimeField()  # hora del turno
    recurrente = models.BooleanField()  # indica si el turno se repite semanalmente
    duracion = models.DurationField(default=timezone.timedelta(hours=1))  # duración del turno (por defecto una hora)
    estado = models.CharField(max_length=1, choices=ESTADO_CHOICES, default='P')  # estado del turno
    evento = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True, blank=True)  # evento asociado al turno

    def __str__(self):
        return f"{self.medico} - {self.fecha} - {self.hora}"

    def save(self, *args, **kwargs):
        # definición del método save
        # agregamos la validación para que no se creen turnos con fechas pasadas
        now = timezone.now()
        turno_datetime = datetime.combine(self.fecha, self.hora)
        if turno_datetime < now:
            raise ValidationError("No se pueden crear turnos con fechas pasadas")
        # validación para evitar cambios en turnos confirmados o atendidos
        if self.estado in ['C', 'A']:
            raise ValidationError("No se pueden modificar turnos confirmados o atendidos")
        calendario = self.medico.calendario
        if self.recurrente:
            rule = Rule(frequency='WEEKLY')
            rule.save()
        else:
            rule = None
        evento = Event.objects.create(
            calendar=calendario,
            title=f"Turno con {self.paciente.nombre}",
            description=f"{self.medico.especialidad}",
            start=turno_datetime,
            end=turno_datetime + self.duracion,
            rule=rule,
        )
        self.evento = evento
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # validación para evitar eliminación de turnos confirmados o atendidos
        if self.estado in ['C', 'A']:
            raise ValidationError("No se pueden eliminar turnos confirmados o atendidos")
        evento = self.evento
        if evento:
            evento.delete()  # eliminar el evento asociado al turno
        super().delete(*args, **kwargs)

    @property
    def get_end_time(self):
        return self.hora + self.duracion  # obtener la hora de finalización del turno

    def get_absolute_url(self):
        return reverse('turno_detail', args=[str(self.id)])  # obtener la URL para acceder al detalle del turno

