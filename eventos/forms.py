from django import forms
from .models import Event , Category, CartItem, Cart
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

class UpdateUserForm(forms.ModelForm):
    group = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True,  # Opcional: si no es obligatorio asignar un grupo
        label="Rol",
    )

    class Meta:
        model = User
        fields = ['username', 'group']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
            
        if commit:
            user.save()  # Guardamos los cambios en el usuario (sin la contraseña en texto claro)
        
        # Asignar el grupo seleccionado
        user.groups.set([self.cleaned_data['group']])  # Asignamos un solo grupo al usuario
        return user

class AddToCartForm(forms.ModelForm):
    quantity = forms.IntegerField(
        min_value=1,
        label="Cantidad",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder':'Cantidad de Entradas'})
    )

    class Meta:
        model = CartItem
        fields = ['quantity']

    def __init__(self, *args, **kwargs):
        self.event = kwargs.pop('event', None) #Se pasa el evento desde la vista
        super().__init__(*args, **kwargs)

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if self.event and quantity > self.event.available_tickets:
            raise forms.ValidationError('No  hay tickets suficientes.')
        return quantity