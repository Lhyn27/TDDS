from django.urls import path
from . import views

urlpatterns = [
<<<<<<< HEAD
    path('', views.EventHomeView.as_view(), name='eventHome'),
    path('list/', views.EventListView.as_view(), name='eventList'),
=======
    path('', views.EventListView.as_view(), name='eventList'),
>>>>>>> 32690f1138692f8d83c7faa2b57cc9ebb9e19fa1
    path('create/', views.EventCreateView.as_view(), name='createEvent'),
]
