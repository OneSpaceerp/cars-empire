from django.urls import path
from . import views

urlpatterns = [
    path('transactions/', views.PaymentTransactionListView.as_view(), name='transaction-list'),
    path('transactions/<int:pk>/', views.PaymentTransactionDetailView.as_view(), name='transaction-detail'),
    path('webhook/', views.PaymentTransactionWebhookView.as_view(), name='payment-webhook'),
] 