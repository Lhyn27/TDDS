from django.db import models

# Create your models here.
class Event(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre")
    image = models.ImageField(upload_to="events/images/", null=True, blank=True, verbose_name="Imagen")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio")
    date = models.DateField(verbose_name="Fecha")
    time = models.TimeField(verbose_name="Hora")
    location = models.CharField(max_length=100, verbose_name="Lugar")
    address = models.CharField(max_length=200, verbose_name="Ubicación")
    category = models.CharField(max_length=100, verbose_name="Categoría")
    available_tickets = models.PositiveIntegerField(verbose_name="Cantidad de entradas")
    description = models.TextField(verbose_name="Descripción")

    def __str__(self):
        return self.name