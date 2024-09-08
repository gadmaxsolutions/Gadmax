from django.shortcuts import render

# Create your views here.


def privacy(request):
    return render(request,'policy/privacy.html')

def refund(request):
    return render(request,'policy/refund.html')

def shipping(request):
    return render(request,'policy/shipping.html')

def terms_conditions(request):
    return render(request,'policy/terms.html')
