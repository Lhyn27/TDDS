from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User

# Formulario para registrar un nuevo usuario
class SignUpForm(UserCreationForm):
    first_name = forms.CharField(
        label='Nombre',
        max_length=30, 
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre'
        })
    )
    last_name = forms.CharField(
        label='Apellido',
        max_length=30, 
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Apellido'
        })
    )
    email = forms.EmailField(
        label='Correo electrónico',
        max_length=254,
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'correo@ejemplo.com'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        labels = {
            'username': 'Nombre de usuario',
            'password1': 'Contraseña',
            'password2': 'Confirmar contraseña'
        }
        help_texts = {
            'username': 'Requerido. 150 caracteres o menos. Letras, números y @/./+/-/_ solamente.',
            'password1': 'Tu contraseña debe contener al menos 8 caracteres y no puede ser demasiado común.',
            'password2': 'Ingresa la misma contraseña para verificación.'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Nombre de usuario'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Contraseña'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirmar contraseña'
        })

        # Personalizar mensajes de error
        self.error_messages = {
            'password_mismatch': 'Las contraseñas no coinciden.',
            'password_too_short': 'La contraseña debe tener al menos 8 caracteres.',
            'password_too_common': 'La contraseña es demasiado común.',
            'password_entirely_numeric': 'La contraseña no puede ser completamente numérica.',
        }

# Formulario para editar el perfil del usuario
class ProfileUpdateForm(UserChangeForm):
    # Quitamos el campo de contraseña que viene por defecto
    password = None
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {
            'username': 'Nombre de usuario',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Correo electrónico'
        }
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de usuario'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Apellido'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'correo@ejemplo.com'
            })
        }
        error_messages = {
            'username': {
                'unique': 'Este nombre de usuario ya está en uso.',
                'required': 'El nombre de usuario es obligatorio.'
            },
            'email': {
                'invalid': 'Por favor, ingresa un correo electrónico válido.',
                'required': 'El correo electrónico es obligatorio.'
            }
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacer el email requerido
        self.fields['email'].required = True
        # Hacer los nombres requeridos
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        
        # Verificar si el email ya existe para otro usuario
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError('Este correo electrónico ya está registrado.')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        # Verificar que el username no contenga caracteres especiales
        if not username.isalnum():
            raise forms.ValidationError('El nombre de usuario solo puede contener letras y números.')
        return username

