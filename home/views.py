from django.core.paginator import Paginator
from django.shortcuts import render,redirect
from store.models import Products, ReviewRating


# Create your views here.

def home(request):
    products=Products.objects.all().filter(is_available = True).order_by('-created_date')
    paginator = Paginator(products, 8)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    reviews=None
    for product in products:
        reviews = ReviewRating.objects.filter(product_id=product.id, status=True)

    context = {
        'products': paged_products,
        'active_page':'home',
        'reviews': reviews,
    }
    return render(request ,'index.html', context)

def about(request):
    return render(request,'about.html')


