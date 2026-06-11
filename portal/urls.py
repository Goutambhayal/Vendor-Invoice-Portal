from django.urls import path
from portal import views

urlpatterns = [
    path('', views.home, name='home'),
    path('freight/', views.freight_view, name='freight'),
    path('invoice-flag/', views.invoice_flag_view, name='invoice_flag'),
]
