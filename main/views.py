from django.shortcuts import render
from .models import Product

# Create your views here.

def home(request):
    products=Product.objects.all()
    return render (request, 'main/pages/home.html', {"products": products})

def set_placeholder_data(request):
    from django.core.files import File
    from django.http import HttpResponse
    import requests
    from io import BytesIO
    import requests

    data = requests.get("https://fakestoreapi.com/products").json()
    for d in data[0:5]:
        title = d["title"]
        price = d["price"]
        description = d["description"]
        image_url = d["image"]
        image = requests.get(image_url).content
        img = File(BytesIO(image), "rb")
        p = Product.objects.create(
            title=title, description=description, price=price, image=img)
        p.save()
    return HttpResponse("data saved")

def buy(request, id):
    product = Product.objects.get(id=id)
    return render (request, 'main/pages/purchase.html', {"product": product})

def profile(request):
    return render (request, 'main/pages/profile.html',{})

def confirmation(request, id):
    product = Product.objects.get(id=id)
    product.stock = product.stock - 1
    product.save()
    return render (request, 'main/pages/confirmation.html', {"product": product})