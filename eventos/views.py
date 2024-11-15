from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.detail import DetailView
from .forms import EventForm , CategoryForm
from .models import Event , Category
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

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
        'mensaje': '''Correo electrónico : contacto@eventosmag.cl
        Número: +56 9 8765 4321'''
    }
    return render(request, 'eventos/contacto.html', context)