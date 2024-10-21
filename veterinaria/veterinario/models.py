from django.db import models
from core.helper_model import ModeloBase
from baseapp.models import Persona, Genero

# Create your models here.
class Veterinario(ModeloBase):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.persona

    class Meta:
        verbose_name = "Veterinario"
        verbose_name_plural = "Veterinarios"

class Propietario(ModeloBase):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.persona.__str__()

    class Meta:
        verbose_name = "Propietario"
        verbose_name_plural = "Propietarios"


class Raza(ModeloBase):
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

class TipoEspecie(ModeloBase):
    nombre = models.CharField(max_length=100, verbose_name="Nombre de la raza", blank=True, null=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Tipo especie"
        verbose_name_plural = "Tipos especie"

class Mascota(ModeloBase):
    propietario = models.ForeignKey(Propietario, on_delete=models.CASCADE, related_name='mascotas', blank=True, null=True)
    nombre = models.CharField(max_length=100, verbose_name="Nombre de la mascota", blank=True, null=True)
    especie = models.ForeignKey(TipoEspecie, on_delete=models.CASCADE, related_name='especiemascota', blank=True, null=True)
    sexo = models.ForeignKey(SexoMascota, on_delete=models.CASCADE, related_name='sexomascota', blank=True, null=True)
    raza = models.ForeignKey(Raza, on_delete=models.CASCADE, related_name='razamascota', blank=True, null=True)
    color = models.CharField(max_length=50, verbose_name="Color", blank=True, null=True)
    fecha_nacimiento = models.DateField(verbose_name="Fecha de nacimiento", blank=True, null=True)
    peso = models.DecimalField(max_digits=25, decimal_places=2, verbose_name="Peso (kg)", blank=True, null=True)

    def __str__(self):
        return f'{self.nombre} ({self.propietario.__str__()})'

    class Meta:
        verbose_name = "Mascota"
        verbose_name_plural = "Mascotas"


class HistorialMedico(models.Model):
    veterinario = models.ForeignKey(Veterinario, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Veterinario responsable")
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE, related_name='historiales', blank=True, null=True)
    descripcion = models.TextField(verbose_name="Descripción del caso", blank=True, null=True)
    fecha_consulta = models.DateField(auto_now_add=True, verbose_name="Fecha de la consulta", blank=True, null=True)
    tratamiento = models.TextField(verbose_name="Tratamiento", blank=True, null=True)
    observaciones = models.TextField(verbose_name="Observaciones", blank=True, null=True)

    def __str__(self):
        return f'Consulta {self.fecha_consulta} - {self.mascota.nombre}'

    class Meta:
        verbose_name = "Historial Médico"
        verbose_name_plural = "Historiales Médicos"

class Producto(models.Model):
    nombre = models.CharField(max_length=200, verbose_name="Nombre del producto", blank=True, null=True)
    descripcion = models.TextField(verbose_name="Descripción del producto", blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio", blank=True, null=True)
    stock = models.IntegerField(verbose_name="Stock disponible", blank=True, null=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"


class Servicio(models.Model):
    nombre = models.CharField(max_length=1000, verbose_name="Nombre del servicio", blank=True, null=True)
    descripcion = models.TextField(verbose_name="Descripción", blank=True, null=True)
    precio = models.DecimalField(max_digits=30, decimal_places=2, verbose_name="Precio", blank=True, null=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Servicio"
        verbose_name_plural = "Servicios"

class Cita(models.Model):
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE, related_name='citas', blank=True, null=True)
    propietario = models.ForeignKey(Propietario, on_delete=models.CASCADE, related_name='citas', blank=True, null=True)
    veterinario = models.ForeignKey("Veterinario", on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Veterinario asignado")
    fecha_cita = models.DateTimeField(verbose_name="Fecha y hora de la cita", blank=True, null=True)
    motivo = models.TextField(verbose_name="Motivo de la cita", blank=True, null=True)

    def __str__(self):
        return f'Cita {self.fecha_cita} - {self.mascota.nombre}'

    class Meta:
        verbose_name = "Cita"
        verbose_name_plural = "Citas"

class DetalleCita(models.Model):
    cita = models.ForeignKey(Cita, on_delete=models.CASCADE, verbose_name="Cita", blank=True, null=True)
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, verbose_name="Servicio", blank=True, null=True)
    cantidad = models.IntegerField(default=1, verbose_name="Cantidad", blank=True, null=True)
    precio_total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio total", blank=True, null=True)

    def __str__(self):
        return f'{self.servicio.nombre} - {self.cita}'

    class Meta:
        verbose_name = "Detalle de la cita"
        verbose_name_plural = "Detalles de las citas"



