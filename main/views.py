from django.shortcuts import render
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


def buy(request, id):
    product = Product.objects.get(id=id)
    return render(request, 'main/pages/purchase.html', {"product": product})


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
    stripe.api_key = settings.STRIPE_API_KEY
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': product.stripe_price_id,
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri(reverse('confirmation')) + '?session_id={CHECKOUT_SESSION_ID}',
        cancle_url=request.build_absolute_uri(reverse('buy')),
    )
    context = {
        'session_id' : session.id,
        'stripe_public_key' : settings.STRIPE_API_KEY,
    }
    print(settings.STRIPE_API_KEY)
    return render(request, 'purchase.html', {"context": context})