from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Medico, HorarioMedico
from .forms import MedicoForm, HorarioMedicoForm,HorarioMedicoUpdateForm

class MedicoListView(ListView):
    model = Medico
    template_name = 'medico_list.html'

class MedicoCreateView(CreateView):
    model = Medico
    form_class = MedicoForm
    template_name = 'medico_form.html'
    success_url = reverse_lazy('medico_list')

class MedicoDetailView(DetailView):
    model = Medico
    template_name = 'medico_detail.html'

class MedicoUpdateView(UpdateView):
    model = Medico
    form_class = MedicoForm
    template_name = 'medico_form.html'
    success_url = reverse_lazy('medico_list')

class MedicoDeleteView(DeleteView):
    model = Medico
    success_url = reverse_lazy('medico_list')
    template_name = 'medico_confirm_delete.html'

# vistas de horarioMedico




class HorarioMedicoListView(ListView):
    model = HorarioMedico
    template_name = 'horario_medico_list.html'
    context_object_name = 'horarios'

    def get_queryset(self):
        # Filtramos los horarios por el id del medico en la URL
        return HorarioMedico.objects.filter(medico=self.kwargs['medico_pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Agregamos el objeto Medico al contexto
        context['medico'] = Medico.objects.get(pk=self.kwargs['medico_pk'])
        return context


class HorarioMedicoCreateView(CreateView):
    model = HorarioMedico
    form_class = HorarioMedicoForm
    template_name = 'horario_medico_form.html'
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Agregamos el objeto Medico al contexto
        context['medico'] = Medico.objects.get(pk=self.kwargs['medico_pk'])
        return context

    def get_success_url(self):
        # Redirigimos a la lista de horarios del medico luego de borrar el horario
        return reverse_lazy('horarios_medicos_list', kwargs={'medico_pk': self.object.medico.pk})


class HorarioMedicoUpdateView(UpdateView):
    model = HorarioMedico
    form_class = HorarioMedicoUpdateForm
    template_name = 'horario_medico_form.html'
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Agregamos el objeto Medico al contexto
        context['medico'] = Medico.objects.get(pk=self.kwargs['medico_pk'])
        return context
    def get_success_url(self):
        # Redirigimos a la lista de horarios del medico luego de borrar el horario
        return reverse_lazy('horarios_medicos_list', kwargs={'medico_pk': self.object.medico.pk})

class HorarioMedicoDeleteView(DeleteView):
    model = HorarioMedico
    template_name = 'horario_medico_confirm_delete.html'
    success_url = reverse_lazy('horarios_medicos_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Agregamos el objeto Medico al contexto
        context['medico'] = Medico.objects.get(pk=self.kwargs['medico_pk'])
        return context

    def get_success_url(self):
        # Redirigimos a la lista de horarios del medico luego de borrar el horario
        return reverse_lazy('horarios_medicos_list', kwargs={'medico_pk': self.object.medico.pk})


class HorarioMedicoDetailView(DetailView):
    model = HorarioMedico
    template_name = 'horario_medico_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Agregamos el objeto Medico al contexto
        context['medico'] = Medico.objects.get(pk=self.kwargs['medico_pk'])
        return context

    
