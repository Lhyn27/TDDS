from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages
from django.db import transaction
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.detail import DetailView
from .forms import EventForm, CategoryForm, UpdateUserForm, AddToCartForm
from .models import Event, Category, Cart, CartItem, Order, OrderItem
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML

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

@method_decorator(login_required, name='dispatch')
class Anadir_Entradas_Carrito(CreateView):
    form_class = AddToCartForm
    template_name = 'eventos/comprar_entrada.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        event = get_object_or_404(Event, pk=self.kwargs['pk'])
        kwargs['event'] = event  # Pasar el evento al formulario
        return kwargs

    def form_valid(self, form):
        event = get_object_or_404(Event, pk=self.kwargs['pk'])
        cart, _ = Cart.objects.get_or_create(user=self.request.user)

        # Agregar o actualizar el item en el carrito
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            event=event,
            defaults={'quantity': form.cleaned_data['quantity']}
        )

        # Si el ítem ya existía, actualizamos su cantidad
        if not created:
            cart_item.quantity = form.cleaned_data['quantity']
            cart_item.save()

        # Redireccionamos después de añadir al carrito
        return redirect('cart_view')

    def form_invalid(self, form):
        # Si el formulario no es válido, renderiza el template con errores
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event'] = get_object_or_404(Event, pk=self.kwargs['pk'])
        return context

@method_decorator(login_required, name='dispatch')
class Listar_Carrito(ListView):
    model = Cart
    template_name = "eventos/carrito.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtener el carrito del usuario autenticado
        cart = Cart.objects.filter(user=self.request.user).first()
        if cart:
            cart_items = CartItem.objects.filter(cart=cart)
            total_price = sum(item.event.price * item.quantity for item in cart_items)
        else:
            cart_items = []
            total_price = 0
        
        # Pasar los datos al contexto
        context['cart'] = cart
        context['cart_items'] = cart_items
        context['total_price'] = total_price
        return context

@method_decorator(login_required, name='dispatch')
class CheckoutView(View):
    template_name = 'eventos/checkout.html'
    
    def get(self, request):
        cart = Cart.objects.filter(user=request.user).first()
        if not cart or not cart.items.exists():
            messages.error(request, "Tu carrito está vacío")
            return redirect('cart_view')
        cart_items = cart.items.all()
        total_price = sum([item.event.price * item.quantity for item in cart_items])
        
        return render(request, "eventos/checkout.html", {'cart': cart, 'total_price': total_price})
    
    def post(self, request):
        cart = Cart.objects.filter(user=request.user).first()
        if not cart or not cart.items.exists():
            messages.error(request, "Tu carrito está vacío")
            return redirect('cart_view')
        
        with transaction.atomic():
            order = Order.objects.create(
                user=request.user,
                total_price=sum(item.event.price * item.quantity for item in cart.items.all()),
                is_completed=True 
            )

            for cart_item in cart.items.all():
                if cart_item.quantity > cart_item.event.available_tickets:
                    messages.error(request, f"No hay suficientes entradas disponibles para {cart_item.event.name}")
                    return redirect('cart_view')
                
                OrderItem.objects.create(
                    order=order,
                    event=cart_item.event,
                    quantity=cart_item.quantity,
                    price=cart_item.event.price
                )

                cart_item.event.available_tickets -= cart_item.quantity
                cart_item.event.save()
            
            cart.items.all().delete()

        messages.success(request, "Compra realizada con éxito.")
        return redirect('order_success', order_id=order.id)

@method_decorator(login_required, name='dispatch')
class OrderSuccessView(View):
    def get(self, request, order_id, *args, **kwargs):
        # Verificar si se requiere generar un PDF
        if 'pdf' in request.GET:
            return self.generar_pdf(order_id)
        
        order = Order.objects.get(id=order_id, user=request.user)
        orderItem = OrderItem.objects.get(id=order_id)
        
        return render(request, 'eventos/order_success.html', {'order': order, 'orderItem': orderItem})

    def generar_pdf(self, order_id):
        # Obtener los datos del modelo
        order = get_object_or_404(Order, id=order_id)
        order_item = get_object_or_404(OrderItem, order=order)
        context = {
            'order': order,
            'orderItem': order_item,
            'pdf': True,  # Indicamos que estamos generando un PDF
        }

        # Renderizar el HTML con la plantilla para el PDF (usa la plantilla existente)
        html_string = render_to_string('eventos/order_success.html', context)

        # Crear la respuesta HTTP con tipo de contenido PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="order.pdf"'

        # Convertir el HTML a PDF usando WeasyPrint
        HTML(string=html_string).write_pdf(response)
        return response
    
@method_decorator(login_required, name='dispatch')
class PurchaseHistoryView(View):
    template_name = 'eventos/historial_compras.html'

    def get(self, request):
        # Obtener todas las órdenes del usuario logueado
        orders = Order.objects.filter(user=request.user).order_by('-created_at')  # Ordenado por la fecha de creación

        return render(request, self.template_name, {'orders': orders})

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
    form_class = UpdateUserForm
    success_url = reverse_lazy('list_user')