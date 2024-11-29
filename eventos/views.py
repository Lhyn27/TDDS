from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.detail import DetailView
from .forms import EventForm, CategoryForm, UserUpdateForm
from .models import Event, Category
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.
class EventListView(ListView):
    model = Event
    template_name = 'eventos/event_list.html'
    context_object_name = 'Events'

@method_decorator(login_required, name='dispatch')
class EventCreateView(CreateView):
    model = Event
    form_class = EventForm
    template_name = 'eventos/event_form.html'
    success_url = reverse_lazy('eventList')

@method_decorator(login_required, name='dispatch')
class EventUpdateView(UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'eventos/event_form.html'
    success_url = reverse_lazy('eventList')

@method_decorator(login_required, name='dispatch')
class EventDeleteView(DeleteView):
    model = Event
    template_name = 'eventos/event_confirm_delete.html'
    context_object_name = 'event'
    success_url = reverse_lazy('eventList')

class EventHomeView(ListView):
    model = Event
    template_name = 'eventos/home.html'
    context_object_name = 'Highlights'

@method_decorator(login_required, name='dispatch')
class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'eventos/create_category.html'
    success_url = reverse_lazy('eventList')

def contacto(request):
    context = {
        'mensaje': 'Correo electrónico : eventos@todoarica.cl' ,
        'mensaje2': 'Número: +56 9 8765 4321'
    }
    return render(request, 'eventos/contacto.html', context)

#función para comprar entradas
def Comprar_Entradas(request, pk):
    #Se Busca el evento específico en la base de datos usando el ID (pk) pasado en la URL
    # Si no se encuentra, devuelve un error 404 (página no encontrada).
    event = get_object_or_404(Event, pk=pk)
    # Si las entradas disponibles son mayores que 0 , se hace el descuento
    if event.available_tickets > 0:
        # Se reducen la cantidad de entradas
        event.available_tickets -= 1
        # se guardan los cambios en la base de datos 
        event.save()
    #redireccion a la lista de eventos
    return redirect('eventList')

@method_decorator(login_required, name='dispatch')
class Listar_Usuario(ListView):
    model = User
    template_name = "eventos/listar_usuario.html"
    context_object_name= 'User'

@method_decorator(login_required, name='dispatch')
class Detalle_Usuario(DetailView):
    model = User
    template_name = 'eventos/detalle_usuario.html'
    context_object_name = 'User'

@method_decorator(login_required, name='dispatch')
class Eliminar_Usuario(DeleteView):
    model = User
    template_name = "eventos/eliminar_usuario.html"
    success_url = reverse_lazy('list_user')

@method_decorator(login_required, name='dispatch')
class Actualizar_Usuario(UpdateView):
    model = User
    template_name = "eventos/actualizar_usuario.html"
    form_class = UserUpdateForm
    success_url = reverse_lazy('list_user')


