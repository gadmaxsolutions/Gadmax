from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from account.models import UserProfile
from cart.models import *
from cart.views import _cart_id
from order.models import OrderProduct
from .forms import ReviewForm
from .models import *
from category.models import *
from brand.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.


def shop(request, category_slug=None, brand_slug=None):
    categories = None
    brands = None
    products = None
    if category_slug or brand_slug :
        if category_slug:
            categories = get_object_or_404(Category, slug=category_slug)
            products = Products.objects.filter(category=categories, is_available=True)

        if brand_slug:
            brands = get_object_or_404(Brand, slug=brand_slug)
            products = Products.objects.filter(brand=brands, is_available=True)

        paginator = Paginator(products, 15)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    else:
        products = Products.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(products, 15)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    context = {
        'products': paged_products,
        'product_count': product_count,
        'active_page': 'shop',
        'categories':categories,
        'brands':brands,

    }
    return render(request, 'store/shop.html', context)


def product_detail(request, category_slug, product_slug):
    try:
        single_product = Products.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
    except Exception as e:
        raise e

    if request.user.is_authenticated:
        try:
            orderproduct = OrderProduct.objects.filter(user=request.user,product_id = single_product.id).exists()
        except OrderProduct.DoesNotExist:
            orderproduct = None
    else:
        orderproduct = None
    # get the reviews
    reviews = ReviewRating.objects.filter(product_id=single_product.id, status=True)
    product_gallery = ProductGallery.objects.filter(product_id=single_product.id)
    rev_count = reviews.count()


    context = {
        'single_product': single_product,
        'in_cart': in_cart,
        'product_gallery': product_gallery,
        'orderproduct': orderproduct,
        'reviews': reviews,
        'rev_count': rev_count,

    }
    return render(request, 'store/product_detail.html', context)


@login_required(login_url='login')
def submit_review(request,product_id):
    url = request.META.get('HTTP_REFERER')# this line helps to stay the same page after submission
    if request.method == "POST":
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id,product__id=product_id)
            form = ReviewForm(request.POST,instance=reviews)
            form.save()
            messages.success(request,"Thank you! Your review has been updated")
            return redirect(url)

        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, "Thank you! Your review has been updated")
                return redirect(url)
