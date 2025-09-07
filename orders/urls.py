from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path('payments/', views.payments, name='payments'),
    path('place_order/', views.place_order, name='place_order'),
    path('order_complete/<str:order_number>/<str:payment_id>/', views.order_complete, name='order_complete'),
]