"""
URL configuration for gadmax project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include

import cart.urls, wishlist.urls, order.urls, account.urls,message.urls,search.urls

import home.urls, store.urls
from django.conf.urls.static import static
from django.conf import settings

import policy.urls

urlpatterns = [
    path('secured_admin/', admin.site.urls),
    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    path('', include(home.urls)),
    path('shop/', include(store.urls, namespace='store_app')),
    path('cart/', include(cart.urls)),
    path('search/', include(search.urls)),
    path('accounts/', include(account.urls)),
    path('wishlist/', include(wishlist.urls)),
    path('orders/', include(order.urls)),
    path('contact/', include(message.urls)),
    path('policy/', include(policy.urls)),
]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
