from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .forms import ProfileUpdateForm
from django.contrib.auth.models import Group


class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/sign_up.html'

    def get_success_url(self):
        return reverse_lazy('login')

    def get_form(self, form_class=None):
        form = super(SignUpView, self).get_form()

        form.fields['username'].widget = forms.TextInput(attrs={'class': 'form-control'})
        form.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control'})
        form.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control'})

        return form

    def form_valid(self, form):
        # Llamamos al método de validación original
        response = super().form_valid(form)
        
        # Obtenemos el grupo 'Usuario' y lo asignamos al nuevo usuario
        group = Group.objects.get(name='Usuario')
        self.object.groups.add(group)
        
        # Guardamos los cambios y devolvemos la respuesta
        self.object.save()

        return response

class ProfileUpdate(UpdateView):
    form_class = ProfileUpdateForm
    success_url = reverse_lazy('home')
    template_name = 'registration/profile.html'


    def get_object(self):
        # No es necesario el get_or_create si solo actualizas el usuario logueado
        return self.request.user 
