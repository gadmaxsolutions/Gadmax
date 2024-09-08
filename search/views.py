from django.shortcuts import render

# Create your views here.
from django.db.models import Q
from django.shortcuts import render

from search.models import SearchLog, FrequentSearch
from store.models import Products


# Create your views here.

def search(request):
    products = Products.objects.none()  # Initialize with an empty queryset
    product_count = 0  # Initialize product count as 0
    context = {}  # Initialize context dictionary

    if 'keyword' in request.GET:
        keyword = request.GET.get('keyword', '')


        try:
            if keyword:
                search_log, created = SearchLog.objects.get_or_create(search_term=keyword)
                if not created:
                    search_log.search_count += 1
                    search_log.save()

                # Move to FrequentSearch if searched more than 3 times
                if search_log.search_count > 3:
                    frequent_search, _ = FrequentSearch.objects.get_or_create(search_term=keyword)
                    search_log.delete()

                products = Products.objects.order_by('-created_date').filter(
                    Q(description__icontains=keyword) |
                    Q(product_name__icontains=keyword)
                )
                product_count = products.count()

        except Exception as e:
            # Log the error if needed
            pass

    # Update the context with products and product_count
    context.update({
        'products': products,
        'product_count': product_count,
    })

    return render(request, 'store/shop.html', context)