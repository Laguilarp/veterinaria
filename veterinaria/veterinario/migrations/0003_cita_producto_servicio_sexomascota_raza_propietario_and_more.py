# Generated by Django 4.2.16 on 2024-10-21 15:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('veterinario', '0002_veterinario_fecha_creacion_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cita',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_cita', models.DateTimeField(blank=True, null=True, verbose_name='Fecha y hora de la cita')),
                ('motivo', models.TextField(blank=True, null=True, verbose_name='Motivo de la cita')),
            ],
            options={
                'verbose_name': 'Cita',
                'verbose_name_plural': 'Citas',
            },
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(blank=True, max_length=200, null=True, verbose_name='Nombre del producto')),
                ('descripcion', models.TextField(blank=True, null=True, verbose_name='Descripción del producto')),
                ('precio', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Precio')),
                ('stock', models.IntegerField(blank=True, null=True, verbose_name='Stock disponible')),
            ],
            options={
                'verbose_name': 'Producto',
                'verbose_name_plural': 'Productos',
            },
        ),
        migrations.CreateModel(
            name='Servicio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Nombre del servicio')),
                ('descripcion', models.TextField(blank=True, null=True, verbose_name='Descripción')),
                ('precio', models.DecimalField(blank=True, decimal_places=2, max_digits=30, null=True, verbose_name='Precio')),
            ],
            options={
                'verbose_name': 'Servicio',
                'verbose_name_plural': 'Servicios',
            },
        ),
        migrations.CreateModel(
            name='SexoMascota',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Fecha creación')),
                ('fecha_modificacion', models.DateTimeField(auto_now=True, null=True, verbose_name='Fecha Modificación')),
                ('status', models.BooleanField(default=True, verbose_name='Estado del registro')),
                ('nombre', models.CharField(blank=True, max_length=100, null=True, verbose_name='Nombre de la raza')),
                ('usuario_creacion', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Usuario Creación')),
                ('usuario_modificacion', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Usuario Modificación')),
            ],
            options={
                'verbose_name': 'Sexo mascota',
                'verbose_name_plural': 'Sexos mascota',
            },
        ),
        migrations.CreateModel(
            name='Raza',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Fecha creación')),
                ('fecha_modificacion', models.DateTimeField(auto_now=True, null=True, verbose_name='Fecha Modificación')),
                ('status', models.BooleanField(default=True, verbose_name='Estado del registro')),
                ('nombre', models.CharField(blank=True, max_length=100, null=True, verbose_name='Nombre de la raza')),
                ('usuario_creacion', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Usuario Creación')),
                ('usuario_modificacion', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Usuario Modificación')),
            ],
            options={
                'verbose_name': 'Raza',
                'verbose_name_plural': 'Razas',
            },
        ),
        migrations.CreateModel(
            name='Propietario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Fecha creación')),
                ('fecha_modificacion', models.DateTimeField(auto_now=True, null=True, verbose_name='Fecha Modificación')),
                ('status', models.BooleanField(default=True, verbose_name='Estado del registro')),
                ('nombre', models.CharField(blank=True, max_length=200, null=True, verbose_name='Nombre completo')),
                ('direccion', models.CharField(blank=True, max_length=300, null=True, verbose_name='Dirección')),
                ('telefono', models.CharField(blank=True, max_length=20, null=True, verbose_name='Teléfono')),
                ('email', models.EmailField(blank=True, max_length=100, null=True, verbose_name='Correo electrónico')),
                ('usuario_creacion', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Usuario Creación')),
                ('usuario_modificacion', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Usuario Modificación')),
            ],
            options={
                'verbose_name': 'Propietario',
                'verbose_name_plural': 'Propietarios',
            },
        ),
        migrations.CreateModel(
            name='Mascota',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Fecha creación')),
                ('fecha_modificacion', models.DateTimeField(auto_now=True, null=True, verbose_name='Fecha Modificación')),
                ('status', models.BooleanField(default=True, verbose_name='Estado del registro')),
                ('nombre', models.CharField(blank=True, max_length=100, null=True, verbose_name='Nombre de la mascota')),
                ('raza', models.CharField(blank=True, max_length=100, null=True, verbose_name='Raza')),
                ('color', models.CharField(blank=True, max_length=50, null=True, verbose_name='Color')),
                ('fecha_nacimiento', models.DateField(blank=True, null=True, verbose_name='Fecha de nacimiento')),
                ('peso', models.DecimalField(blank=True, decimal_places=2, max_digits=25, null=True, verbose_name='Peso (kg)')),
                ('especie', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='raza', to='veterinario.raza')),
                ('propietario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mascotas', to='veterinario.propietario')),
                ('sexo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sexomascota', to='veterinario.sexomascota')),
                ('usuario_creacion', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Usuario Creación')),
                ('usuario_modificacion', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Usuario Modificación')),
            ],
            options={
                'verbose_name': 'Mascota',
                'verbose_name_plural': 'Mascotas',
            },
        ),
        migrations.CreateModel(
            name='HistorialMedico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.TextField(blank=True, null=True, verbose_name='Descripción del caso')),
                ('fecha_consulta', models.DateField(auto_now_add=True, null=True, verbose_name='Fecha de la consulta')),
                ('tratamiento', models.TextField(blank=True, null=True, verbose_name='Tratamiento')),
                ('observaciones', models.TextField(blank=True, null=True, verbose_name='Observaciones')),
                ('mascota', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='historiales', to='veterinario.mascota')),
                ('veterinario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='veterinario.veterinario', verbose_name='Veterinario responsable')),
            ],
            options={
                'verbose_name': 'Historial Médico',
                'verbose_name_plural': 'Historiales Médicos',
            },
        ),
        migrations.CreateModel(
            name='DetalleCita',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField(blank=True, default=1, null=True, verbose_name='Cantidad')),
                ('precio_total', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Precio total')),
                ('cita', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='veterinario.cita', verbose_name='Cita')),
                ('servicio', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='veterinario.servicio', verbose_name='Servicio')),
            ],
            options={
                'verbose_name': 'Detalle de la cita',
                'verbose_name_plural': 'Detalles de las citas',
            },
        ),
        migrations.AddField(
            model_name='cita',
            name='mascota',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='citas', to='veterinario.mascota'),
        ),
        migrations.AddField(
            model_name='cita',
            name='propietario',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='citas', to='veterinario.propietario'),
        ),
        migrations.AddField(
            model_name='cita',
            name='veterinario',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='veterinario.veterinario', verbose_name='Veterinario asignado'),
        ),
    ]
