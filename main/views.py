from django.shortcuts import render, redirect
from .models import Product
from django.http import Http404
from django.conf import settings
import stripe
from django.contrib.auth.decorators import login_required
from django.urls import reverse


def home(request):
    products = Product.objects.all()
    return render(request, 'main/pages/home.html', {"products": products})


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


# def buy(request, id):
#     product = Product.objects.get(id=id)
#     return render(request, 'main/pages/purchase.html', {"product": product})


def profile(request):
    return render(request, 'main/pages/profile.html', {})


def confirmation(request, id):
    product = Product.objects.get(id=id)
    if product.stock <= 0:
        raise Http404
    else:
        product.stock = product.stock - 1
        product.save()
        return render(request, 'main/pages/confirmation.html', {"product": product})


def checkout(request, id):
    product = Product.objects.get(id=id)
    stripe.api_key = settings.STRIPE_PRIVATE_KEY
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items = [
            {
                'price': product.stripe_price_id,
                'quantity': 1
            }
        ],
        mode = 'payment',
        success_url = "https://127.0.0.1:8000/payment/success?session_id={CHECKOUT_SESSION_ID}",
        cancel_url = "https://127.0.0.1:8000/payment/cancel"
    )
    context = {
        "session_id": checkout_session.id,
        "stripe_public_key": settings.STRIPE_PUBLIC_KEY,
        "product": product
        
    }
    return render(request, 'main/pages/purchase.html', context)
