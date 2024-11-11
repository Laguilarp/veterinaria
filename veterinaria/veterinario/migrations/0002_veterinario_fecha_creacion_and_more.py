# Generated by Django 4.2.16 on 2024-10-21 15:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('veterinario', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='veterinario',
            name='fecha_creacion',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Fecha creación'),
        ),
        migrations.AddField(
            model_name='veterinario',
            name='fecha_modificacion',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='Fecha Modificación'),
        ),
        migrations.AddField(
            model_name='veterinario',
            name='status',
            field=models.BooleanField(default=True, verbose_name='Estado del registro'),
        ),
        migrations.AddField(
            model_name='veterinario',
            name='usuario_creacion',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Usuario Creación'),
        ),
        migrations.AddField(
            model_name='veterinario',
            name='usuario_modificacion',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Usuario Modificación'),
        ),
    ]
