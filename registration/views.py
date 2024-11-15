from django import forms
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
<<<<<<< HEAD

=======
>>>>>>> 32690f1138692f8d83c7faa2b57cc9ebb9e19fa1
# Create your views here.

class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/sign_up.html'
    
    def get_success_url(self) -> str:
        return reverse_lazy('login')
    
    def get_form(self, form_class = None):
        form = super(SignUpView, self).get_form()
        
        form.fields['username'].widget = forms.TextInput(attrs={'class':'form-control'})
        form.fields['password1'].widget = forms.PasswordInput(attrs={'class':'form-control'})
        form.fields['password2'].widget = forms.PasswordInput(attrs={'class':'form-control'})
        
        return form