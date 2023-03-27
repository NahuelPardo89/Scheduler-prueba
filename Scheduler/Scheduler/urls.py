"""Scheduler URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from SchedulerPrueba.views import ( MedicoListView, MedicoCreateView, MedicoDetailView, 
                                    MedicoUpdateView, MedicoDeleteView,
                                    HorarioMedicoListView,HorarioMedicoCreateView,HorarioMedicoUpdateView,
                                    HorarioMedicoDeleteView,HorarioMedicoDetailView
                                    )








urlpatterns = [
    path('admin/', admin.site.urls),
    path('medicos/', MedicoListView.as_view(), name='medico_list'),
    path('medicos/crear/', MedicoCreateView.as_view(), name='medico_create'),
    path('medicos/<int:pk>/', MedicoDetailView.as_view(), name='medico_detail'),
    path('medicos/<int:pk>/actualizar/', MedicoUpdateView.as_view(), name='medico_update'),
    path('medicos/<int:pk>/borrar/', MedicoDeleteView.as_view(), name='medico_delete'),

    path('medicos/<int:medico_pk>/horarios/', HorarioMedicoListView.as_view(), name='horarios_medicos_list'),
    path('medicos/<int:medico_pk>/horarios/crear/', HorarioMedicoCreateView.as_view(), name='horarios_medicos_create'),
    path('medicos/<int:medico_pk>/horarios/<int:pk>/editar/', HorarioMedicoUpdateView.as_view(), name='horarios_medicos_update'),
    path('medicos/<int:medico_pk>/horarios/<int:pk>/eliminar/', HorarioMedicoDeleteView.as_view(), name='horarios_medicos_delete'),
    path('medicos/<int:medico_pk>/horarios/<int:pk>/', HorarioMedicoDetailView.as_view(), name='horarios_medicos_detail'),
]
