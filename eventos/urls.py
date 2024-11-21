from django.urls import path
from eventos import views

urlpatterns = [
    path('', views.EventHomeView.as_view(), name='eventHome'),
    path('list/', views.EventListView.as_view(), name='eventList'),
    path('create/', views.EventCreateView.as_view(), name='createEvent'),
    path('update/<int:pk>', views.EventUpdateView.as_view(), name='updateEvent'),
    path('delete/<int:pk>', views.EventDeleteView.as_view(), name='deleteEvent'),
    path('create_category/', views.CategoryCreateView.as_view(), name='createCategory'),
    path('contacto/', views.contacto, name='contacto'),
    path('evento/comprar_entrada/<int:pk>/', views.Comprar_Entradas, name='buy_ticket')

]
