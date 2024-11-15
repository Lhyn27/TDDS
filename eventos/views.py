from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.detail import DetailView
from .forms import EventForm
from .models import Event
<<<<<<< HEAD
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
=======
>>>>>>> 32690f1138692f8d83c7faa2b57cc9ebb9e19fa1

# Create your views here.
class EventListView(ListView):
    model = Event
    template_name = 'eventos/event_list.html'
    context_object_name = 'Events'
<<<<<<< HEAD
@method_decorator(login_required, name='dispatch')
=======

>>>>>>> 32690f1138692f8d83c7faa2b57cc9ebb9e19fa1
class EventCreateView(CreateView):
    model = Event
    form_class = EventForm
    template_name = 'eventos/event_form.html'
    success_url = reverse_lazy('eventList')

<<<<<<< HEAD
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
    success_url = reverse_lazy('eventList')


=======
>>>>>>> 32690f1138692f8d83c7faa2b57cc9ebb9e19fa1
class EventHomeView(ListView):
    model = Event
    template_name = 'eventos/home.html'
    context_object_name = 'Highlights'