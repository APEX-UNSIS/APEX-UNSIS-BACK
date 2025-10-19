from django.db import models
from django.contrib.auth.models import User

class Periodos(models.Model):
    id_periodo = models.CharField(max_length=20, primary_key=True)
    nombre_periodo = models.CharField(max_length=30)

    class Meta:
        verbose_name = 'Periodo'
        verbose_name_plural = 'Periodos'

    def __str__(self):
        return self.nombre_periodo

class TipoEvaluacion(models.Model):
    id_evaluacion = models.CharField(max_length=20, primary_key=True)
    nombre_evaluacion = models.CharField(max_length=30)

    class Meta:
        verbose_name = 'Tipo de Evaluación'
        verbose_name_plural = 'Tipos de Evaluaciones'

    def __str__(self):
        return self.nombre_evaluacion

class Grupos(models.Model):
    id_grupo = models.CharField(max_length=20, primary_key=True)
    nombre_grupo = models.CharField(max_length=20)

    class Meta:
        verbose_name = 'Grupo'
        verbose_name_plural = 'Grupos'

    def __str__(self):
        return self.nombre_grupo

class Materias(models.Model):
    id_materia = models.CharField(max_length=20, primary_key=True)
    nombre_materia = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Materia'
        verbose_name_plural = 'Materias'

    def __str__(self):
        return self.nombre_materia

class Profesores(models.Model):
    id_profesor = models.CharField(max_length=20, primary_key=True)
    # Vínculo con el sistema de usuarios de Django
    user = models.OneToOneField(
        User, 
        on_delete=models.SET_NULL, # Si se borra el User, no se borra el Profesor
        null=True, 
        blank=True
    )
    nombre_profesor = models.CharField(max_length=60)
    is_disable = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Profesor'
        verbose_name_plural = 'Profesores'

    def __str__(self):
        return self.nombre_profesor

class Aulas(models.Model):
    id_aula = models.CharField(max_length=20, primary_key=True)
    nombre_aula = models.CharField(max_length=50)
    is_disable = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Aula'
        verbose_name_plural = 'Aulas'

    def __str__(self):
        return self.nombre_aula


class HorarioExamen(models.Model):
    id_horario = models.CharField(max_length=20, primary_key=True)
    
    
    periodo = models.ForeignKey(
        Periodos, 
        on_delete=models.PROTECT, # No dejar borrar un periodo si tiene horarios
        db_column='id_periodo'
    )
    evaluacion = models.ForeignKey(
        TipoEvaluacion, 
        on_delete=models.PROTECT, # No dejar borrar un tipo de eval si tiene horarios
        db_column='id_evaluacion'
    )
    grupo = models.ForeignKey(
        Grupos, 
        on_delete=models.CASCADE, # Si se borra el grupo, se borra el horario
        db_column='id_grupo'
    )
    materia = models.ForeignKey(
        Materias, 
        on_delete=models.PROTECT, # No dejar borrar una materia si tiene horarios
        db_column='id_materia'
    )
    profesor = models.ForeignKey(
        Profesores, 
        on_delete=models.SET_NULL, # Si se borra el profesor, el campo se pone nulo
        null=True, 
        db_column='id_profesor',
        related_name='horarios_como_principal' # Necesario porque 'Profesor' se usa 2 veces
    )
    aula = models.ForeignKey(
        Aulas, 
        on_delete=models.SET_NULL, # Si se borra el aula, el campo se pone nulo
        null=True, 
        db_column='id_aula'
    )
    profesor_sinodal = models.ForeignKey(
        Profesores,
        on_delete=models.SET_NULL,
        null=True,
        blank=True, # 'blank=True' permite que sea opcional
        db_column='id_profesor_sinodal',
        related_name='horarios_como_sinodal' # Necesario
    )
    
    # --- Campos de Fecha y Hora ---
    fecha_examen = models.DateField()
    hora_examen = models.TimeField()

    class Meta:
        verbose_name = 'Horario de Examen'
        verbose_name_plural = 'Horarios de Exámenes'
        
        # Opcional: Evita duplicados
        constraints = [
            models.UniqueConstraint(
                fields=['periodo', 'evaluacion', 'grupo', 'materia'], 
                name='horario_unico_por_materia_grupo'
            )
        ]

    def __str__(self):
        return f"{self.materia.nombre_materia} - {self.grupo.nombre_grupo} ({self.periodo.nombre_periodo})"