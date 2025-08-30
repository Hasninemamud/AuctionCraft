from django.urls import path
from . import views

urlpatterns = [
    path('create-payment-intent/', views.create_payment_intent, name='create_payment_intent'),
    path('confirm-order/', views.confirm_order, name='confirm_order'),
]
