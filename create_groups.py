import os
import django

# Configura Django antes de interactuar con el ORM
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EventosTicketCompra.settings')
django.setup()

from django.contrib.auth.models import Group

def create_default_groups():
    # Lista de grupos a crear
    groups = ['Usuario', 'Organizador de Eventos']
    
    #Mensaje que sale en la consola al crearse los grupos indicados en este script 
    for group_name in groups:
        group, created = Group.objects.get_or_create(name=group_name)
        if created:
            print(f"Grupo '{group_name}' creado.")
        else:
            print(f"Grupo '{group_name}' ya existe.")

if __name__ == '__main__':
    create_default_groups()
