from django.contrib import admin
from .models import Medico, HorarioMedico, Paciente,Turno
# Register your models here.
admin.site.register(Medico)
admin.site.register(HorarioMedico)
admin.site.register( Paciente)
admin.site.register(Turno)
