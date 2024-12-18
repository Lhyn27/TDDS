from django import forms
from .models import Event, Category, CartItem, Cart
from django.contrib.auth.models import User , Group
from datetime import datetime

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
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'min': datetime.today().date() }),
            'time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
            'available_tickets': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        error_messages = {
            'name': {'required': 'Este campo es obligatorio.'},
            'image': {'required': 'Debe agregar una imagen al evento'},
            'price': {'required': 'Debes ingresar un precio válido.'},
            'address': {'required': 'Debe ingresar una dirección para el evento'},
            'category': {'required': 'Debe escoger al menos una categoría'},
            'avilable_tickets': {'required': 'Debe agregar la cantidad de entradas para el evento'},
            'description': {'required': 'Debe agregar una descripción del evento'}
        }

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        time = cleaned_data.get('time')
        
        # Lista de caracteres invisibles y especiales a eliminar
        INVISIBLE_CHARS = [
            '\u200E',  # LEFT-TO-RIGHT MARK
            '\u200F',  # RIGHT-TO-LEFT MARK
            '\u200B',  # ZERO WIDTH SPACE
            '\u200C',  # ZERO WIDTH NON-JOINER
            '\u200D',  # ZERO WIDTH JOINER
            '\uFEFF',  # ZERO WIDTH NO-BREAK SPACE
            '\u202A',  # LEFT-TO-RIGHT EMBEDDING
            '\u202B',  # RIGHT-TO-LEFT EMBEDDING
            '\u202C',  # POP DIRECTIONAL FORMATTING
            '\u202D',  # LEFT-TO-RIGHT OVERRIDE
            '\u202E',  # RIGHT-TO-LEFT OVERRIDE
        ]
        
        # Limpiar espacios y caracteres especiales en campos de texto
        text_fields = ['name', 'address', 'description']
        for field in text_fields:
            if value := cleaned_data.get(field):
                cleaned_value = value.strip()
                for char in INVISIBLE_CHARS:
                    cleaned_value = cleaned_value.replace(char, '')
                cleaned_data[field] = cleaned_value
        
        if not date or not time:
            return cleaned_data
            
        current_date = datetime.today().date()
        current_time = datetime.now().time()
        
        # Validar que la fecha no sea anterior a hoy
        if date < current_date:
            self.add_error('date', 'La fecha no puede ser anterior al día de hoy.')
            
        # Si la fecha es hoy, validar que la hora sea posterior a la actual
        if date == current_date:
            # Convertir las horas a minutos para una comparación más precisa
            event_minutes = time.hour * 60 + time.minute
            current_minutes = current_time.hour * 60 + current_time.minute
            
            if event_minutes <= current_minutes:
                self.add_error('time', f'Para eventos de hoy, la hora debe ser posterior a {current_time.strftime("%H:%M")}')
        
        return cleaned_data
    
    def clean_image(self):
        image = self.cleaned_data.get('image')
        if not image:
            raise forms.ValidationError("Debe agregar una imagen al evento.")
        return image


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