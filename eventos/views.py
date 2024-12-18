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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_organizer'] = self.request.user.groups.filter(name='Organizador de Eventos').exists()
        return context

@method_decorator(login_required, name='dispatch')
class EventCreateView(CreateView):
    model = Event
    form_class = EventForm
    template_name = 'eventos/event_form.html'
    success_url = reverse_lazy('eventList')

    def form_valid(self, form):
        form.instance.organizer = self.request.user
        return super().form_valid(form)

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
    
    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')

        if action:
            item_id = action.split('_')[1]
            cart_item = CartItem.objects.get(id=item_id, cart__user=request.user)

            if 'increase' in action:
                cart_item.quantity += 1
            elif 'decrease' in action and cart_item.quantity > 1:
                cart_item.quantity -= 1
            elif 'delete' in action:
                cart_item.delete()
                return redirect('cart_view')
            
            cart_item.save()
        
        return redirect('cart_view')

def luhn_algorithm(card_number):
    card_number = card_number.replace(" ", "")
    if not card_number.isdigit():
        return False
    
    total = 0
    reverse_digits = card_number[::-1]
    for i, digit in enumerate(reverse_digits):
        n = int(digit)
        if i % 2 == 1:
            n *= 2
            if n > 9:
                n -= 9
        total += n
    return total % 10 == 0

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
        
        # Prellenar con datos del usuario
        initial_data = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        }
        
        return render(request, self.template_name, {
            'cart': cart, 
            'cart_items': cart_items,
            'total_price': total_price,
            'form_data': initial_data
        })
    
    def post(self, request):
        try:
            with transaction.atomic():
                # Verificar que hay items antes de crear la orden
                cart = Cart.objects.filter(user=request.user).first()
                if not cart or not cart.items.exists():
                    messages.error(request, "Tu carrito está vacío")
                    return redirect('cart_view')

                # Calcular el total antes de crear la orden
                total_price = sum(item.event.price * item.quantity for item in cart.items.all())
                
                # Solo crear la orden si hay un total válido
                if total_price > 0:
                    order = Order.objects.create(
                        user=request.user,
                        total_price=total_price,
                        is_completed=True 
                    )

                    # Crear los items de la orden
                    for cart_item in cart.items.all():
                        if cart_item.quantity > cart_item.event.available_tickets:
                            raise ValueError(f"No hay suficientes entradas disponibles para {cart_item.event.name}")
                        
                        OrderItem.objects.create(
                            order=order,
                            event=cart_item.event,
                            quantity=cart_item.quantity,
                            price=int(cart_item.event.price)
                        )

                        cart_item.event.available_tickets -= cart_item.quantity
                        cart_item.event.save()
                    
                    # Limpiar el carrito solo si todo fue exitoso
                    cart.items.all().delete()
                    
                    messages.success(request, "Compra realizada con éxito.")
                    return redirect('order_success', order_id=order.id)
                else:
                    messages.error(request, "El total de la orden debe ser mayor a 0")
                    return redirect('cart_view')
                    
        except ValueError as e:
            messages.error(request, str(e))
            return redirect('cart_view')
        except Exception as e:
            messages.error(request, "Error al procesar la compra. Por favor, intente nuevamente.")
            return redirect('checkout')

@method_decorator(login_required, name='dispatch')
class OrderSuccessView(View):
    def get(self, request, order_id, *args, **kwargs):
        # Verificar si se requiere generar un PDF
        if 'pdf' in request.GET:
            return self.generar_pdf(order_id)
        
        # Obtener la orden
        order = get_object_or_404(Order, id=order_id)
        
        # Verificar permisos
        if not (request.user.is_staff or 
                request.user == order.user or 
                (request.user.groups.filter(name='Organizador de Eventos').exists() and 
                 order.orderitem_set.filter(event__organizer=request.user).exists())):
            messages.error(request, "No tienes permiso para ver esta orden")
            return redirect('eventHome')
        
        order_items = OrderItem.objects.filter(order=order)
        total_tickets = sum(item.quantity for item in order_items)
        
        return render(request, 'eventos/order_success.html', {
            'order': order,
            'order_items': order_items,
            'total_tickets': total_tickets
        })

    def generar_pdf(self, order_id):
        # Obtener los datos del modelo
        order = get_object_or_404(Order, id=order_id)
        order_items = OrderItem.objects.filter(order=order)
        total_tickets = sum(item.quantity for item in order_items)
        context = {
            'order': order,
            'order_item': order_items,
            'total_tickets': total_tickets,
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

    def get_queryset(self):
        return User.objects.filter(groups__name='Usuario')

@method_decorator(login_required, name='dispatch')
class Listar_Trabajadores(ListView):
    model = User
    template_name = "eventos/listar_trabajadores.html"
    context_object_name = "Worker"
    
    def get_queryset(self):
        return User.objects.exclude(groups__name='Usuario')

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

@method_decorator(login_required, name='dispatch')
class AdminPurchaseHistoryView(View):
    template_name = 'eventos/admin_purchase_history.html'

    def get(self, request):
        if request.user.is_staff:
            # Admin ve todas las compras
            orders = Order.objects.all().prefetch_related(
                'items', 
                'items__event'
            ).order_by('-created_at')
        elif request.user.groups.filter(name='Organizador de Eventos').exists():
            # Organizador ve solo las compras de sus eventos
            orders = Order.objects.filter(
                items__event__organizer=request.user
            ).prefetch_related(
                'items', 
                'items__event'
            ).distinct().order_by('-created_at')
        else:
            messages.error(request, "No tienes permiso para ver esta página")
            return redirect('eventHome')

        # Debug: Imprimir información sobre las órdenes
        print(f"Número de órdenes: {orders.count()}")
        for order in orders:
            print(f"Orden {order.id}: {order.items.count()} items")

        return render(request, self.template_name, {
            'orders': orders,
            'is_admin': request.user.is_staff
        })

@method_decorator(login_required, name='dispatch')
class EventDetailView(DetailView):
    model = Event
    template_name = 'eventos/event_detail.html'
    context_object_name = 'event'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Verificar si el usuario es organizador o admin
        context['can_edit'] = (
            self.request.user.is_staff or 
            self.request.user.groups.filter(name='Organizador de Eventos').exists()
        )
        return context