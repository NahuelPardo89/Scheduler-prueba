from django import forms
from .models import Medico,HorarioMedico


class MedicoForm(forms.ModelForm):
    class Meta:
        model = Medico
        fields = ['dni','nombre', 'especialidad']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'especialidad': forms.TextInput(attrs={'class': 'form-control'}),
            'calendario': forms.HiddenInput(),
        }
        help_texts = {
            'nombre': '<span class="help-block">Ingrese el nombre del médico.</span>',
            'especialidad': '<span class="help-block">Ingrese la especialidad del médico.</span>',
        }
        error_messages = {
            'nombre': {
                'required': 'Este campo es obligatorio',
            },
            'especialidad': {
                'required': 'Este campo es obligatorio',
            },
        }




class HorarioMedicoForm(forms.ModelForm):
    DIA_SEMANA_CHOICES = [
        (0, 'Lunes'),
        (1, 'Martes'),
        (2, 'Miércoles'),
        (3, 'Jueves'),
        (4, 'Viernes'),
        (5, 'Sábado'),
        (6, 'Domingo'),
    ]
    
    dia_semana = forms.ChoiceField(
        choices=DIA_SEMANA_CHOICES, 
        widget=forms.Select(attrs={'class': 'form-control'}), 
        label='Día de la semana',
        help_text='Seleccione el día de la semana para el que desea agregar el horario.'
    )

    class Meta:
        model = HorarioMedico
        fields = ['medico','dia_semana', 'hora_inicio', 'hora_fin']
        widgets = {
            'hora_inicio': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'hora_fin': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        }
        error_messages = {
            'hora_inicio': {
                'invalid': 'Ingrese una hora válida en formato HH:MM (ej: 08:00, 09:30).',
            },
            'hora_fin': {
                'invalid': 'Ingrese una hora válida en formato HH:MM (ej: 08:00, 09:30).',
            },
        }
        
    def clean(self):
        cleaned_data = super().clean()
        horario = HorarioMedico(
            medico=self.cleaned_data.get('medico'),
            dia_semana=cleaned_data['dia_semana'],
            hora_inicio=cleaned_data['hora_inicio'],
            hora_fin=cleaned_data['hora_fin']
        )
        if horario.horario_superpuesto():
            raise forms.ValidationError("Este horario se superpone con otro horario existente")
        if horario.hora_inicio >= horario.hora_fin:
            raise forms.ValidationError("La hora de inicio debe ser anterior a la hora de fin")
        if horario.hora_fin.minute != 0:
            raise forms.ValidationError("La hora de fin debe ser en punto (ej: 08:00, 09:00)")
        return cleaned_data

class HorarioMedicoUpdateForm(forms.ModelForm):
    class Meta:
        model = HorarioMedico
        fields = ['hora_inicio', 'hora_fin']
        widgets = {
            'hora_inicio': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'hora_fin': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        }
        error_messages = {
            'hora_inicio': {
                'invalid': 'Ingrese una hora válida en formato HH:MM (ej: 08:00, 09:30).',
            },
            'hora_fin': {
                'invalid': 'Ingrese una hora válida en formato HH:MM (ej: 08:00, 09:30).',
            },
        }
    
    def clean(self):
        cleaned_data = super().clean()
        hora_inicio = cleaned_data.get('hora_inicio')
        hora_fin = cleaned_data.get('hora_fin')
        if hora_inicio and hora_fin and hora_inicio >= hora_fin:
            raise forms.ValidationError("La hora de inicio debe ser anterior a la hora de fin")
        if hora_fin and hora_fin.minute != 0:
            raise forms.ValidationError("La hora de fin debe ser en punto (ej: 08:00, 09:00)")
        return cleaned_data