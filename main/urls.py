from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('store/', views.set_placeholder_data, name='store'),
    #path('purchase/<id>', views.buy, name='buy'),
    path('accounts/profile/', views.profile, name='profile'),
    path('confirmation/<id>', views.confirmation, name='confirmation'),
    path('checkout/<id>', views.checkout, name='checkout'),
    path('payment/success', views.success, name='success'),
    path('check/', views.check, name="check"),
]
