import datetime
import json
import logging
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
import razorpay
from django.views.decorators.csrf import csrf_exempt
from .forms import *
from cart.models import CartItem, BuyDirect
from .models import Order
from gadmax.settings import RZP_KEY_ID,RZP_KEY_SECRET

client = razorpay.Client(auth=(RZP_KEY_ID, RZP_KEY_SECRET))



def order_complete(request):
    order_id = request.GET.get('order_id')

    try:
        order = Order.objects.get(order_number=order_id, is_ordered=True)
        ordered_products = OrderProduct.objects.filter(order=order)
        sub_total = 0
        grand_total=0
        for i in ordered_products:
            sub_total+=(i.price*i.quantity)

        grand_total = sub_total
        context = {
            'order': order,
            'ordered_products': ordered_products,
            'order_number': order.order_number,
            'sub_total': sub_total,

            'grand_total': grand_total,

        }
        return render(request, 'order/order_complete.html', context)
    except Order.DoesNotExist:
        return redirect('home')


logger = logging.getLogger(__name__)


@csrf_exempt
def payment(request):
    current_user = request.user
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            razorpay_payment_id = data.get('razorpay_payment_id')
            razorpay_order_id = data.get('razorpay_order_id')
            razorpay_signature = data.get('razorpay_signature')

            # Verify the Razorpay signature
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            }

            try:
                client.utility.verify_payment_signature(params_dict)
            except razorpay.errors.SignatureVerificationError as e:
                logger.error(f"Payment verification failed: {e}")
                return JsonResponse({'success': False, 'error': 'Payment verification failed'}, status=400)

            # Fetch the order
            orders = Order.objects.filter(user=current_user, is_ordered=False)

            if orders.exists():
                order = orders.first()  # Assuming you handle only the first order for simplicity

                # Save the payment details
                payment = Payment.objects.create(
                    user=current_user,
                    order_id=order.order_number,  # Use order.order_number
                    razorpay_payment_id=razorpay_payment_id,
                    razorpay_order_id=razorpay_order_id,
                    razorpay_signature=razorpay_signature,
                    amount_paid=order.order_total,  # Use order.order_total
                    status='Completed',
                )

                payment.save()
                order.is_ordered = True
                order.status = 'Completed'
                order.save()

                # Handle BuyDirect item if it exists
                buy_direct_item = BuyDirect.objects.filter(user=current_user, is_active=True).first()
                if buy_direct_item:
                    orderproduct = OrderProduct()
                    orderproduct.order_id = order.id
                    orderproduct.payment_id = payment
                    orderproduct.user_id = current_user.id
                    orderproduct.product_id = buy_direct_item.product_id
                    orderproduct.quantity = buy_direct_item.quantity
                    orderproduct.price = buy_direct_item.product.price
                    orderproduct.ordered = True
                    orderproduct.save()

                    product_variation = buy_direct_item.variations.all()
                    orderproduct.variation.set(product_variation)
                    orderproduct.save()

                    # Reduce the quantity of sold products
                    product = Products.objects.get(id=buy_direct_item.product_id)
                    product.stock -= buy_direct_item.quantity
                    product.save()

                    # Deactivate the BuyDirect item
                    buy_direct_item.is_active = False
                    buy_direct_item.save()

                # Move the cart items to the order product table
                cart_items = CartItem.objects.filter(user=current_user)
                for item in cart_items:
                    orderproduct = OrderProduct()
                    orderproduct.order_id = order.id
                    orderproduct.payment_id = payment
                    orderproduct.user_id = current_user.id
                    orderproduct.product_id = item.product_id
                    orderproduct.quantity = item.quantity
                    orderproduct.price = item.product.price
                    orderproduct.ordered = True
                    orderproduct.save()

                    cart_item = CartItem.objects.get(id=item.id)
                    product_variation = cart_item.variations.all()
                    orderproduct = OrderProduct.objects.get(id=orderproduct.id)
                    orderproduct.variation.set(product_variation)
                    orderproduct.save()

                    # Reduce the quantity of sold products
                    product = Products.objects.get(id=item.product_id)
                    product.stock -= item.quantity
                    product.save()

                # Clear the cart
                CartItem.objects.filter(user=current_user).delete()

                # Send order received email to customer
                mail_subject = 'Thank you for Shopping with us'
                message = render_to_string('order/order_received_email.html', {
                    'user': current_user,
                    'order': order,
                })
                to_email = current_user.email
                send_email = EmailMessage(mail_subject, message, to=[to_email])
                send_email.send()

                # Redirect to the order complete page
                return redirect(f'/orders/order_complete/?order_id={order.order_number}')
            else:
                return JsonResponse({'success': False, 'error': 'No pending order found'}, status=404)

        except razorpay.errors.SignatureVerificationError as e:
            return JsonResponse({'success': False, 'error': 'Payment verification failed: ' + str(e)}, status=400)

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)

    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)





@login_required(login_url='login')
def place_order(request, total=0, quantity=0):
    current_user = request.user

    # Check for BuyDirect items
    buy_direct_item = BuyDirect.objects.filter(user=current_user, is_active=True).first()

    # if buy_direct_item:
    # Handle the direct buy scenario
    total = buy_direct_item.product.price * buy_direct_item.quantity
    quantity = buy_direct_item.quantity
    grand_total = total

    # Proceed with order placement
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            # Store billing information
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.mobile_no = form.cleaned_data['mobile_no']
            data.email = form.cleaned_data['email']
            data.address_1 = form.cleaned_data['address_1']
            data.address_2 = form.cleaned_data['address_2']
            data.street = form.cleaned_data['street']
            data.city = form.cleaned_data['city']
            data.district = form.cleaned_data['district']
            data.state = form.cleaned_data['state']
            data.country = form.cleaned_data['country']
            data.pincode = form.cleaned_data['pincode']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()

            # Generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime("%Y%m%d")
            order_num = current_date + str(data.id)
            data.order_number = order_num
            data.save()

            # Payment handling
            DATA = {
                "amount": float(data.order_total) * 100,
                "currency": "INR",
                "receipt": "receipt #" + data.order_number,
                "notes": {
                    "key1": "value3",
                    "key2": "value2"
                }
            }

            # Create an order in payment gateway
            rzp_order = client.order.create(data=DATA)

            rzp_order_id = rzp_order['id']

            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_num)

            context = {
                'order': order,
                'buy_direct_item': buy_direct_item,
                'total': total,
                'rzp_order_id': rzp_order_id,
                'grand_total': grand_total,
                'RZP_KEY_ID': RZP_KEY_ID,
                'RZP_KEY_SECRET': RZP_KEY_SECRET,
                "RZP_AMOUNT": float(data.order_total) * 100
            }
            return render(request, 'order/confirm.html', context)



    return redirect('checkout')