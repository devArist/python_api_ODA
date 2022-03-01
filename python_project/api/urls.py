from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('', views.HomeAPIView.as_view(), name='home'),
    path('customers/', views.CustomersAPIView.as_view(), name='customers'),
    path('customers/<int:pk>', views.CustomerAPIView.as_view(), name='customers'),
]