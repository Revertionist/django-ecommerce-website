from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('store/', views.set_placeholder_data),
    path('purchase/<id>', views.buy),
    path('accounts/profile/', views.profile),
    path('confirmation/<id>', views.confirmation),
]
