from django import forms
from core.helper_form import FormBase
from baseapp.models import Persona, Genero

class PersonaForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = [
                    'nombres', 'apellido1', 'apellido2', 'tipodocumento', 'documento', 'genero',
                    'fecha_nacimiento', 'direccion', 'correo_electronico', 'telefono'
                 ]

        error_messages = {
            'persona': {
                'unique': "Ya existe persona registrada con este nombre."
            }
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['documento'].max_length = 10
        self.fields['telefono'].max_length = 10
        # Agregar clases CSS específicas a cada campo
        self.fields['nombres'].widget.attrs.update({'class': 'form-control', 'col': 'col-md-12', 'required':'true'})
        self.fields['apellido1'].widget.attrs.update({'class': 'form-control', 'col': 'col-md-6', 'required':'true'})
        self.fields['apellido2'].widget.attrs.update({'class': 'form-control', 'col': 'col-md-6', 'required':'true'})
        self.fields['tipodocumento'].widget.attrs.update({'class': 'form-control', 'data-live-search':'true', 'col': 'col-md-6', 'required':'true'})
        self.fields['documento'].widget.attrs.update({'class': 'form-control', 'col': 'col-md-4', 'maxlength': '10'})
        self.fields['direccion'].widget.attrs.update({'class': 'form-control', 'col': 'col-md-12', 'required':'true'})
        self.fields['genero'].widget.attrs.update({'class': 'form-control', 'data-live-search':'true', 'col': 'col-md-6', 'required':'true'})
        self.fields['fecha_nacimiento'].widget.attrs.update({'class': 'form-control date', 'col': 'col-md-6', 'type': 'date', 'format': 'yyyy-mm-dd', 'required':'true'})
        self.fields['correo_electronico'].widget.attrs.update({'class': 'form-control', 'col': 'col-md-6'})
        self.fields['telefono'].widget.attrs.update({'class': 'form-control', 'col': 'col-md-6', 'maxlength': '10'})

        self.fields['genero'].queryset = Genero.objects.filter(status=True)


    def bloquear_campos(self):
        self.fields['nombres'].widget.attrs.update({'class': 'form-control', 'col': 'col-md-12', 'required': 'False', 'readonly': 'true'})
        self.fields['apellido1'].widget.attrs.update({'class': 'form-control', 'col': 'col-md-12', 'required': 'False', 'readonly': 'true'})
        self.fields['apellido2'].widget.attrs.update({'class': 'form-control', 'col': 'col-md-12', 'required': 'False', 'readonly': 'true'})