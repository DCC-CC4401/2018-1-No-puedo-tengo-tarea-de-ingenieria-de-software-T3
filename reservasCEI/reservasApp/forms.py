from django import forms
from django.core.validators import RegexValidator
from django.forms import ModelForm
from reservasApp.models import Person
from django.contrib.auth import password_validation

class EspacioForm(forms.Form):
    #your_name = forms.CharField(label='Your name', max_length=100)
    espacio_id = forms.IntegerField()

class NewPersonForm(ModelForm):
    error_messages = {
        'password_mismatch': "Las contraseñas no son iguales.",
    }
    
    username = forms.CharField(label='RUT ',
                               widget=forms.TextInput(
                                   attrs={
                                       'class':'form-control',
                                       'autofocus': True
                                   }
                               ),
                               validators=[RegexValidator(
                                  regex='\d(\d?)[.](\d{3})[.](\d{3})[-](\d|[kK])',
                                  message='Debe ingresar el rut con puntos y digito verificador. (Por ejemplo: 12.345.678-9)',
                                  code='invalid_username'),],
                               help_text='Tu RUT con puntos, guion y digito verificador.',
                              )
    
    first_name = forms.CharField(label='Nombre',
                                 widget=forms.TextInput(
                                     attrs={'class':'form-control'}
                                 ),
                                )
    
    last_name = forms.CharField(label='Apellido',
                                 widget=forms.TextInput(
                                     attrs={'class':'form-control'}
                                 )
                                )
    
    password1 = forms.CharField(label='Contraseña',
                                 widget=forms.PasswordInput(
                                     attrs={'class':'form-control'}
                                 ),
                                strip=False,
                                help_text='Por lo menos 8 caracteres.',
                                )
    
    password2 = forms.CharField(label='Confirmar contraseña',
                                 widget=forms.PasswordInput(
                                     attrs={'class':'form-control'}
                                 ),
                                strip=False,
                                help_text='Repite la contraseña para verificarla.',
                                )
    
    email = forms.EmailField(label='Correo', widget=forms.EmailInput(
        attrs={
            'class':'form-control'
        }
    ))
    
    class Meta:
        model = Person
        fields = ['username', 'first_name', 'last_name', 'email']
        
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2
    
    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get('password2')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except forms.ValidationError as error:
                self.add_error('password2', error)
                
    def save(self, commit=True):
        person = super().save(commit=False)
        person.set_password(self.cleaned_data["password1"])
        if commit:
            person.save()
        return person