from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre")

    def __str__(self):
        return self.name

class Event(models.Model):
    organizer = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name='events')
    name = models.CharField(max_length=100, verbose_name="Nombre")
    image = models.ImageField(upload_to="events/images/", null=True, blank=True, verbose_name="Imagen")
    price = models.IntegerField(verbose_name='Precio')
    date = models.DateField(verbose_name="Fecha")
    time = models.TimeField(verbose_name="Hora")
    address = models.CharField(max_length=200, verbose_name="Ubicación")
    category = models.ManyToManyField(Category, verbose_name='Categorias')
    available_tickets = models.PositiveIntegerField(verbose_name="Cantidad de entradas")
    description = models.TextField(verbose_name="Descripción")

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')

    def __str__(self) -> str:
        return f"Carrito de {self.user.username}"
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self) -> str:
        return f"{self.quantity} x {self.event.name}"
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.IntegerField()
    is_completed = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"Pedido #{self.id} - {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price =  models.IntegerField()

    def get_subtotal(self):
        return self.quantity * self.price
    
    def __str__(self) -> str:
        return f"{self.quantity} x {self.event.name} - ${self.get_subtotal()}"