# Generated by Django 4.2.16 on 2024-10-21 15:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('baseapp', '0005_alter_genero_fecha_creacion_and_more'),
        ('veterinario', '0003_cita_producto_servicio_sexomascota_raza_propietario_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='propietario',
            name='direccion',
        ),
        migrations.RemoveField(
            model_name='propietario',
            name='email',
        ),
        migrations.RemoveField(
            model_name='propietario',
            name='nombre',
        ),
        migrations.RemoveField(
            model_name='propietario',
            name='telefono',
        ),
        migrations.AddField(
            model_name='propietario',
            name='persona',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='baseapp.persona'),
        ),
    ]