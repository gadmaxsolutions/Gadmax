from django.urls import path
from . import views


urlpatterns = [
    path('privacy-policy/',views.privacy,name="privacy"),
    path('refund-policy/',views.refund,name="refund"),
    path('shipping-policy/',views.shipping,name="shipping"),
    path('terms_and_conditions/',views.terms_conditions,name="terms_conditions"),
]