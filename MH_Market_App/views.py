from django.shortcuts import render, redirect
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Max, Min
from cart.cart import Cart



# Create your views here.?
def base(request):
    return render(request, 'base.html')

def home(request):
    sliders = Slider.objects.all().order_by('-id')[0:3]
    banners = Banner.objects.all().order_by('-id')[0:3]
    main_category = Main_Category.objects.all().order_by('-id')
    product = Product.objects.filter(section__name='Top Deals Of The Day')

    context = {
        'sliders':sliders,
        'banners':banners,
        'main_category':main_category,
        'product':product,
    }
    return render(request, 'home.html', context)


def product_detail(request, slug):
    product = Product.objects.filter(slug=slug)
    if product.exists():
        product = Product.objects.get(slug=slug)
    else:
        return redirect('error_404')
    context = {
        'product':product,
    }
    return render(request, 'product_detail.html', context)


def error_404(request):
    return render(request, '404.html')


def registration(request):
    if request.method == "GET":
        form = CustomerRegistrationForm()
        return render(request, 'registration.html', {'form':form})
    elif request.method == "POST":
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulations!! Registered Successfully')
            form.save()
        return render(request, 'registration.html', {'form':form})
 

@login_required
def profile(request):
    if request.method == "GET":
        form = CustomerProfileForm()
        return render(request, 'profile.html', {'form':form})
    elif request.method == "POST":
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name =form.cleaned_data['name']
            locality =form.cleaned_data['locality']
            city =form.cleaned_data['city']
            zipcode =form.cleaned_data['zipcode']
            reg = Customer(user=usr, name=name, locality=locality, city=city, zipcode=zipcode)
            reg.save()
            messages.success(request, 'Congratulations!! Profile Updated Successfully')
        return render(request, 'profile.html', {'form':form})
 

def about_us(request):
    return render(request, 'about_us.html')


def contact_us(request):
    return render(request, 'contact_us.html')


def product(request):
    category = Category.objects.all()
    product = Product.objects.all()
    min_price = Product.objects.all().aggregate(Min('price'))
    max_price = Product.objects.all().aggregate(Max('price'))
    FilterPrice = request.GET.get('FilterPrice')
    if FilterPrice:
        Int_FilterPrice = int(FilterPrice)
        product = Product.objects.filter(price__lte = Int_FilterPrice)
    else:
        product = Product.objects.all()

    context = {
        'category':category,
        'product':product,
        'min_price':min_price,
        'max_price':max_price,
        'FilterPrice':FilterPrice,
    }
    return render(request, 'product.html', context)


def filter_data(request):
    categories = request.GET.getlist('category[]')
    brands = request.GET.getlist('brand[]')
    allProducts = Product.objects.all().order_by('-id').distinct()
    if len(categories) > 0:
        allProducts = allProducts.filter(category__id__in=categories).distinct()

    if len(brands) > 0:
        allProducts = allProducts.filter(Brand__id__in=brands).distinct()
    t = render_to_string('ajax_product_filter.html', {'product': allProducts})
    return JsonResponse({'data': t})



@login_required
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required
def cart_detail(request):
    return render(request, 'cart.html')


def checkout(request):
    return render(request, 'checkout.html')


def wishlist(request):
    return render(request, 'wishlist.html')


def faq(request):
    return render(request, 'faq.html')


