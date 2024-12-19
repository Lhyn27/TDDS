from django.urls import path
from eventos import views

urlpatterns = [
    #Path de eventos
    path('', views.EventHomeView.as_view(), name='eventHome'),
    path('list/', views.EventListView.as_view(), name='eventList'),
    path('create/', views.EventCreateView.as_view(), name='createEvent'),
    path('event/<int:pk>/', views.EventDetailView.as_view(), name='event_detail'),
    path('update/<int:pk>', views.EventUpdateView.as_view(), name='updateEvent'),
    path('delete/<int:pk>', views.EventDeleteView.as_view(), name='deleteEvent'),
    path('create_category/', views.CategoryCreateView.as_view(), name='createCategory'),
    #Path de cliente
    path('evento/comprar_entrada/<int:pk>/', views.Anadir_Entradas_Carrito.as_view(), name='buy_ticket'),
    path('eventos/carrito',views.Listar_Carrito.as_view() ,name='cart_view'),
    path('eventos/checkout', views.CheckoutView.as_view(), name='checkout'),
    path('order-success/<int:order_id>', views.OrderSuccessView.as_view(), name='order_success'),
    path('mis-compras/', views.PurchaseHistoryView.as_view(), name='historial_compras'),
    #Path de User
    path('list_usuario/', views.Listar_Usuario.as_view(), name='list_user'),
    path('list_trabajador/', views.Listar_Trabajadores.as_view(), name='list_worker'),
    path('detalle_usuario/<int:pk>/', views.Detalle_Usuario.as_view(), name='detalle_user'),
    path('actualizar_usuario/<int:pk>/', views.Actualizar_Usuario.as_view(), name='actualizar_user'),
    path('eliminar_usuario/<int:pk>/', views.Eliminar_Usuario.as_view(), name='eliminar_user'),
    path('admin_purchase_history/', views.AdminPurchaseHistoryView.as_view(), name='admin_purchase_history'),
    path('analytics/', views.AnalyticsView.as_view(), name='analytics'),
]
