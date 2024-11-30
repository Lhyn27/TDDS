from django.urls import path
from eventos import views

urlpatterns = [
    #Path de eventos
    path('', views.EventHomeView.as_view(), name='eventHome'),
    path('list/', views.EventListView.as_view(), name='eventList'),
    path('create/', views.EventCreateView.as_view(), name='createEvent'),
    path('update/<int:pk>', views.EventUpdateView.as_view(), name='updateEvent'),
    path('delete/<int:pk>', views.EventDeleteView.as_view(), name='deleteEvent'),
    path('create_category/', views.CategoryCreateView.as_view(), name='createCategory'),
    path('contacto/', views.contacto, name='contacto'),
    #Path de cliente
    path('evento/comprar_entrada/<int:pk>/', views.Anadir_Entradas_Carrito.as_view(), name='buy_ticket'),
    path('eventos/carrito',views.Listar_Carrito.as_view() ,name='cart_view'),
    #Path de User
    path('list_usuario/', views.Listar_Usuario.as_view(), name='list_user'),
    path('detalle_usuario/<int:pk>/', views.Detalle_Usuario.as_view(), name='detalle_user'),
    path('actualizar_usuario/<int:pk>/', views.Actualizar_Usuario.as_view(), name='actualizar_user'),
    path('eliminar_usuario/<int:pk>/', views.Eliminar_Usuario.as_view(), name='eliminar_user')

]
