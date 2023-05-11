from django.shortcuts import render
from .models import Product
import json
# Create your views here.

def home(request):
    products=Product.objects.get(id=2)
    return render (request, 'main/pages/home.html', {"product": products})