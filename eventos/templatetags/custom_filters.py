from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    """Multiplica el valor por el argumento"""
    try:
        return value * arg
    except (TypeError, ValueError):
        return None

@register.filter
def map(value, arg):
    """Aplica una funcion (pasada como argumento) a una lista"""
    return list(map(arg, value))

@register.filter
def sum(value, arg):
    """Suma los elementos de una lista"""
    return sum(value)