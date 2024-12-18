from django.db import models
from core.helper_model import ModeloBase
from baseapp.models import Persona, Genero

# Create your models here.
class Veterinario(ModeloBase):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.persona.__str__()

    class Meta:
        verbose_name = "Veterinario"
        verbose_name_plural = "Veterinarios"

class Propietario(ModeloBase):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, blank=True, null=True)
    mascota = models.ManyToManyField("veterinario.Mascota", related_name='mascotapropietario')

    def __str__(self):
        return self.persona.__str__()

    class Meta:
        verbose_name = "Propietario"
        verbose_name_plural = "Propietarios"

    def get_mis_mascotas(self):
        return self.mascota.filter(status=True).count()

class TipoEspecie(ModeloBase):
    nombre = models.CharField(max_length=100, verbose_name="Nombre de la especie", blank=True, null=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Tipo especie"
        verbose_name_plural = "Tipos especie"

class Raza(ModeloBase):
    especie = models.ForeignKey("veterinario.TipoEspecie", on_delete=models.CASCADE, blank=True, null=True, verbose_name='tipoespecie')
    nombre = models.CharField(max_length=100, verbose_name="Nombre de la raza", blank=True, null=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Raza"
        verbose_name_plural = "Razas"


class SexoMascota(ModeloBase):
    nombre = models.CharField(max_length=100, verbose_name="Nombre de la raza", blank=True, null=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Sexo mascota"
        verbose_name_plural = "Sexos mascota"

class Mascota(ModeloBase):
    #propietario = models.ForeignKey(Propietario, on_delete=models.CASCADE, related_name='mascotas', blank=True, null=True)
    nombre = models.CharField(max_length=100, verbose_name="Nombre de la mascota", blank=True, null=True)
    sexo = models.ForeignKey(SexoMascota, on_delete=models.CASCADE, related_name='sexomascota', blank=True, null=True)
    especie = models.ForeignKey(TipoEspecie, on_delete=models.CASCADE, related_name='tipoespecie', blank=True, null=True)
    raza = models.ForeignKey(Raza, on_delete=models.CASCADE, related_name='razamascota', blank=True, null=True)
    color = models.CharField(max_length=50, verbose_name="Color", blank=True, null=True)
    fechanacimiento = models.DateField(verbose_name="Fecha de nacimiento", blank=True, null=True)
    peso = models.DecimalField(max_digits=25, decimal_places=2, verbose_name="Peso (kg)", blank=True, null=True)

    def __str__(self):
        return f'{self.nombre}'

    class Meta:
        verbose_name = "Mascota"
        verbose_name_plural = "Mascotas"

    def get_propietario(self):
        prop = Propietario.objects.filter(status=True, mascota__id=self.id)
        if prop.exists():
            prop = prop.first()
            return prop
        return ''

    def get_historialmedico(self):
        return HistorialMedico.objects.filter(status=True, mascota=self)

    def get_historialdesparasitacion(self):
        return HistorialDesparasitante.objects.filter(status=True, mascota=self)

    def get_historialvacunacion(self):
        return HistorialVacunacion.objects.filter(status=True, mascota=self)


class HistorialMedico(ModeloBase):
    veterinario = models.ForeignKey(Veterinario, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Veterinario responsable")
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE, related_name='mascotahistorialmedico', blank=True, null=True)
    descripcion = models.TextField(verbose_name="Descripción del caso", blank=True, null=True)
    fecha_consulta = models.DateField(auto_now_add=True, verbose_name="Fecha de la consulta", blank=True, null=True)
    tratamiento = models.ManyToManyField("veterinario.Tratamiento", blank=True, null=True)
    inyeccion = models.ManyToManyField("veterinario.Inyeccion", blank=True, null=True)
    medicamento = models.CharField(verbose_name="Medicamento", blank=True, null=True)
    dosis = models.CharField(verbose_name="Dosis", blank=True, null=True)
    prescripcion = models.CharField(verbose_name="Prescripción", blank=True, null=True)

    def __str__(self):
        return f'Consulta {self.fecha_consulta} - {self.descripcion}'

    class Meta:
        verbose_name = "Historial Médico"
        verbose_name_plural = "Historiales Médicos"

    def get_medicacion(self):
        return MedicacionDetalleCita.objects.filter(status=True, historial=self)

class HistorialDesparasitante(ModeloBase):
    veterinario = models.ForeignKey(Veterinario, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Veterinario responsable")
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE, related_name='historiales', blank=True, null=True)
    fecha = models.DateField(verbose_name=u"Fecha desparasitación", blank=True, null=True)
    edad = models.IntegerField(default=0, verbose_name=u'Edad en años')
    peso = models.FloatField(default=0, blank=True, null=True, verbose_name="Peso en kg")
    desparasitante = models.ForeignKey("veterinario.Desparasitante", on_delete=models.CASCADE, verbose_name="Desparasitante", blank=True, null=True)
    fechaproximadesparasitante = models.DateField(verbose_name=u"Fecha próxima desparasitación", blank=True, null=True)

class HistorialVacunacion(ModeloBase):
    veterinario = models.ForeignKey(Veterinario, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Veterinario responsable")
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE, related_name='mascotavacunacion', blank=True, null=True)
    fecha = models.DateField(verbose_name=u"Fecha desparasitación", blank=True, null=True)
    edad = models.IntegerField(default=0, verbose_name=u'Edad en años')
    peso = models.FloatField(default=0, blank=True, null=True, verbose_name="Peso en kg")
    vacuna = models.ForeignKey("veterinario.Inyeccion", on_delete=models.CASCADE, blank=True, null=True, verbose_name=u"Vacuna")
    lote = models.TextField(verbose_name="Lote", blank=True, null=True)
    fechafab = models.DateField(verbose_name=u"Fecha Fb.", blank=True, null=True)
    fechaproximavacuna = models.DateField(verbose_name=u"Fecha próxima vacuna", blank=True, null=True)

    def get_vacunacion(self):
        return VacunacionDetalleCita.objects.filter(status=True, historial=self)


class Producto(ModeloBase):
    nombre = models.CharField(max_length=200, verbose_name="Nombre del producto", blank=True, null=True)
    descripcion = models.TextField(verbose_name="Descripción del producto", blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio", blank=True, null=True)
    stock = models.IntegerField(verbose_name="Stock disponible", blank=True, null=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"


class Tratamiento(ModeloBase):
    nombre = models.CharField(max_length=1000, verbose_name="Nombre del servicio", blank=True, null=True)
    precio = models.DecimalField(max_digits=30, decimal_places=2, verbose_name="Precio", blank=True, null=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Servicio"
        verbose_name_plural = "Servicios"

class Inyeccion(ModeloBase):
    descripcion = models.TextField(verbose_name="Descripción", blank=True, null=True)
    precio = models.DecimalField(max_digits=30, decimal_places=2, verbose_name="Precio", blank=True, null=True)

    def __str__(self):
        return f'{self.descripcion}'

ESTADO_CITA = (
    (1, u'PENDIENTE'),
    (2, u'APROBADO'),
    (3, u'RECHAZADO'),
    (4, u'ELIMINADO'),
)

MOTIVO_CITA = (
    (1, u'VACUNACIÓN'),
    (2, u'DESPARASITACIÓN'),
    (3, u'CONTROL MÉDICO'),
)

class Cita(ModeloBase):
    propietario = models.ForeignKey(Propietario, on_delete=models.CASCADE, related_name='propietariocita', blank=True, null=True)
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE, related_name='citas', blank=True, null=True)
    veterinario = models.ForeignKey("Veterinario", on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Veterinario asignado")
    fecha_cita = models.DateField(verbose_name="Fecha de la cita", blank=True, null=True)
    hora_cita = models.TimeField(verbose_name="Hora de la cita", blank=True, null=True)
    motivocita = models.IntegerField(choices=MOTIVO_CITA, default=1, verbose_name=u'Motivo de la cita')
    motivo = models.TextField(verbose_name="Observacion", blank=True, null=True)
    estado = models.IntegerField(choices=ESTADO_CITA, default=1, verbose_name=u'Estado')

    def get_color_estado(self):
        color = 'danger'
        if self.estado == 2:
            color = 'success'
        return color

    def __str__(self):
        return f'Cita {self.fecha_cita} - {self.mascota.nombre}'

    class Meta:
        verbose_name = "Cita"
        verbose_name_plural = "Citas"

    def get_propietario(self):
        prop = Propietario.objects.filter(status=True, mascota__id=self.mascota.id)
        if prop.exists():
            prop = prop.first()
            return prop
        return ''

class Desparasitante(ModeloBase):
    nombre = models.CharField(max_length=2000, verbose_name="Nombre del desparasitante", blank=True, null=True)

    def __str__(self):
        return f'{self.nombre}'

    class Meta:
        verbose_name = "Desparasitante"
        verbose_name_plural = "Desparasitantes"

class DetalleCita(ModeloBase):
    cita = models.ForeignKey(Cita, on_delete=models.CASCADE, verbose_name="Cita", blank=True, null=True)
    tratamiento = models.ManyToManyField(Tratamiento, blank=True, null=True, verbose_name="Medicamento")
    inyeccion = models.ManyToManyField(Inyeccion, blank=True, null=True)
    observacion = models.TextField(verbose_name="Observación", blank=True, null=True)
    precio_total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio total", blank=True, null=True)

    #CAMPOS GENERALES
    fecha = models.DateField(verbose_name=u"Fecha", blank=True, null=True)
    edad = models.IntegerField(default=0, verbose_name=u'Edad en años')
    peso = models.FloatField(default=0, blank=True, null=True, verbose_name="Peso en kg")

    #DESPARASITACION
    desparasitante = models.ForeignKey(Desparasitante, on_delete=models.CASCADE, verbose_name="Desparasitante", blank=True, null=True)
    fechaproximadesparasitante = models.DateField(verbose_name=u"Fecha próxima desparasitación", blank=True, null=True)

    #VACUNACIÓN
    vacuna = models.ForeignKey("veterinario.Inyeccion", related_name='vacunaaplicada', on_delete=models.CASCADE, blank=True, null=True, verbose_name=u"Vacuna")
    lote = models.CharField(verbose_name="Lote", blank=True, null=True)
    fechafab = models.DateField(verbose_name=u"Fecha Fb.", blank=True, null=True)
    fechaproximavacuna = models.DateField(verbose_name=u"Fecha próxima vacuna", blank=True, null=True)

    #CONTROL MÉDICO
    medicamento = models.CharField(verbose_name="Medicamento", blank=True, null=True)
    dosis = models.CharField(verbose_name="Dosis", blank=True, null=True)
    prescripcion = models.CharField(verbose_name="Prescripción", blank=True, null=True)



    def __str__(self):
        return f'{self.observacion}'

    class Meta:
        verbose_name = "Detalle de la cita"
        verbose_name_plural = "Detalles de las citas"

class Medicacion(ModeloBase):
    descripcion = models.TextField(verbose_name="Descripción", blank=True, null=True)

    def __str__(self):
        return f'{self.descripcion}'

    class Meta:
        verbose_name = "Medicación"
        verbose_name_plural = "Medicaciones"


class MedicacionDetalleCita(ModeloBase):
    historial = models.ForeignKey(HistorialMedico, on_delete=models.CASCADE, related_name='historialmedico', verbose_name="Historial médico", blank=True, null=True)
    medicamento = models.ForeignKey(Medicacion, related_name='medicamentoaplicadadetalle', on_delete=models.CASCADE, blank=True, null=True, verbose_name=u"Medicamento")
    dosis = models.CharField(verbose_name="Dosis", blank=True, null=True)
    prescripcion = models.CharField(verbose_name="Prescripción", blank=True, null=True)

    def __str__(self):
        return f'{self.medicamento}'

    class Meta:
        verbose_name = "Medicación"
        verbose_name_plural = "Medicaciones"

class VacunaDetalleCita(ModeloBase):
    detalle = models.ForeignKey(DetalleCita, on_delete=models.CASCADE, related_name='detallevacuna', verbose_name="Detalle cita", blank=True, null=True)
    vacuna = models.ForeignKey("veterinario.Inyeccion", related_name='vacunaaplicadadetalle', on_delete=models.CASCADE, blank=True, null=True, verbose_name=u"Vacuna")
    lote = models.CharField(verbose_name="Lote", blank=True, null=True)
    fechafab = models.DateField(verbose_name=u"Fecha Fb.", blank=True, null=True)
    fechaproximavacuna = models.DateField(verbose_name=u"Fecha próxima vacuna", blank=True, null=True)

    def __str__(self):
        return f'{self.vacuna}'

    class Meta:
        verbose_name = "Medicación"
        verbose_name_plural = "Medicaciones"

class VacunacionDetalleCita(ModeloBase):
    historial = models.ForeignKey(HistorialVacunacion, on_delete=models.CASCADE, related_name='historialvacunacion', verbose_name="Historial vacunación", blank=True, null=True)
    vacuna = models.ForeignKey(Inyeccion, related_name='vacunaaplicadadetallee', on_delete=models.CASCADE, blank=True, null=True, verbose_name=u"Vacuna")
    lote = models.TextField(verbose_name="Lote", blank=True, null=True)
    fechafab = models.DateField(verbose_name=u"Fecha Fb.", blank=True, null=True)
    fechaproximavacuna = models.DateField(verbose_name=u"Fecha próxima vacuna", blank=True, null=True)

    def __str__(self):
        return f'{self.vacuna}'

    class Meta:
        verbose_name = "Vacuna aplicada"
        verbose_name_plural = "Vacunas aplicadas"



