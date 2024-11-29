from django import forms
from .models import Event , Category
from django.contrib.auth.models import User , Group

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'name', 
            'image', 
            'price', 
            'date', 
            'time', 
            'address', 
            'category', 
            'available_tickets', 
            'description'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'available_tickets': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']  
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
        }

class UserUpdateForm(forms.ModelForm):
    password = forms.CharField(
        label="Nueva contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False,  # La contraseña es opcional al actualizar
    )
    group = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True,  # Opcional: si no es obligatorio asignar un grupo
        label="Rol",
    )

    class Meta:
        model = User
        fields = ['username', 'password', 'group']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        
        # Si la contraseña se ha proporcionado, la actualizamos
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)  # Asegúrate de encriptar la nueva contraseña
            
        if commit:
            user.save()  # Guardamos los cambios en el usuario (sin la contraseña en texto claro)
        
        # Asignar el grupo seleccionado
        user.groups.set([self.cleaned_data['group']])  # Asignamos un solo grupo al usuario
        return user
