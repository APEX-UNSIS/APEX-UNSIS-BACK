from django.contrib import admin
from .models import Periodos, TipoEvaluacion, Grupos, Materias, Aulas, Profesores, HorarioExamen

# Esto "expone" tus modelos al panel de admin
admin.site.register(Periodos)
admin.site.register(TipoEvaluacion)
admin.site.register(Grupos)
admin.site.register(Materias)
admin.site.register(Aulas)
admin.site.register(Profesores)
admin.site.register(HorarioExamen)

# Register your models here.
