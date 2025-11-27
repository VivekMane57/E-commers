# # accounts/views.py
# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib import messages, auth
# from django.contrib.auth.decorators import login_required
# from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
# from django.utils.encoding import force_bytes
# from django.template.loader import render_to_string
# from django.contrib.auth.tokens import default_token_generator
# from django.contrib.sites.shortcuts import get_current_site
# from django.core.mail import EmailMessage
# from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
# from django.views.decorators.csrf import csrf_exempt
# from django.contrib.auth import update_session_auth_hash
# from django.core.exceptions import ImproperlyConfigured
# from django.conf import settings
# from django.db import transaction
# from django.db.models import Count
# from django.urls import reverse

# import json
# import requests
# import razorpay
# from datetime import datetime
# import uuid

# from .forms import RegistrationForm, UserForm, UserProfileForm
# from .models import Account, UserProfile
# from carts.models import Cart, CartItem
# from carts.views import _cart_id
# from orders.models import Order, OrderProduct, Payment


# # -------------------- Razorpay Client Setup --------------------
# def get_razorpay_client():
#     """Initialize and return Razorpay client"""
#     try:
#         key = getattr(settings, 'RAZORPAY_KEY_ID', None)
#         secret = getattr(settings, 'RAZORPAY_KEY_SECRET', None)
        
#         if not key or not secret:
#             raise ImproperlyConfigured("Razorpay keys are missing from settings")
            
#         return razorpay.Client(auth=(key, secret))
#     except Exception as e:
#         raise ImproperlyConfigured(f"Error initializing Razorpay client: {str(e)}")


# # ====================== AUTHENTICATION VIEWS ====================== 
# def register(request):
#     """User registration view with referral system"""
#     if request.method == 'POST':
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             try:
#                 with transaction.atomic():
#                     first_name = form.cleaned_data['first_name']
#                     last_name = form.cleaned_data['last_name']
#                     phone_number = form.cleaned_data['phone_number']
#                     email = form.cleaned_data['email']
#                     password = form.cleaned_data['password']
#                     username = email.split("@")[0]

#                     # Create user
#                     user = Account.objects.create_user(
#                         first_name=first_name,
#                         last_name=last_name,
#                         email=email,
#                         username=username,
#                         password=password
#                     )
#                     user.phone_number = phone_number

#                     # Handle referral code
#                     ref_code = form.cleaned_data.get('referral_code')
#                     if ref_code:
#                         try:
#                             referring_user = Account.objects.get(referral_code=ref_code)
#                             user.referred_by = referring_user
#                         except Account.DoesNotExist:
#                             messages.warning(request, 'Invalid referral code')

#                     user.save()

#                     # Create user profile
#                     UserProfile.objects.create(user=user)

#                     # Send activation email
#                     try:
#                         current_site = get_current_site(request)
#                         mail_subject = 'Activate your account'
#                         message = render_to_string('accounts/account_verification_email.html', {
#                             'user': user,
#                             'domain': current_site.domain,
#                             'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#                             'token': default_token_generator.make_token(user),
#                         })
#                         EmailMessage(mail_subject, message, to=[email]).send()
#                         messages.success(request, 'Registration successful! Please check your email.')
#                     except Exception as e:
#                         messages.warning(request, 'Account created but verification email failed.')

#                     return redirect('accounts:login')
                    
#             except Exception as e:
#                 messages.error(request, f'Registration failed: {str(e)}')
                
#     else:
#         form = RegistrationForm()
#         ref_code = request.GET.get('ref')
#         if ref_code:
#             form.fields['referral_code'].initial = ref_code

#     return render(request, 'accounts/register.html', {'form': form})


# def login(request):
#     """User login view with cart merging"""
#     if request.method == 'POST':
#         email = request.POST.get('email', '').strip()
#         password = request.POST.get('password', '').strip()
        
#         if not email or not password:
#             messages.error(request, "Please fill in both fields")
#             return redirect('accounts:login')
            
#         user = auth.authenticate(email=email, password=password)

#         if user is not None:
#             if user.is_active:
#                 # Merge guest cart with user cart
#                 try:
#                     guest_cart = Cart.objects.get(cart_id=_cart_id(request))
#                     if CartItem.objects.filter(cart=guest_cart).exists():
#                         guest_items = CartItem.objects.filter(cart=guest_cart)
#                         user_items = CartItem.objects.filter(user=user)
                        
#                         # Get variations for comparison
#                         guest_variations = [list(item.variations.all()) for item in guest_items]
#                         user_variations = [list(item.variations.all()) for item in user_items]
                        
#                         # Merge items
#                         for i, g_variation in enumerate(guest_variations):
#                             if g_variation in user_variations:
#                                 index = user_variations.index(g_variation)
#                                 user_item = user_items[index]
#                                 user_item.quantity += guest_items[i].quantity
#                                 user_item.save()
#                                 guest_items[i].delete()
#                             else:
#                                 guest_items[i].user = user
#                                 guest_items[i].save()
#                 except Exception:
#                     # Cart merging failed, but continue with login
#                     pass

#                 auth.login(request, user)
#                 messages.success(request, f"Welcome back, {user.first_name}!")

#                 # Redirect to next URL or dashboard
#                 next_url = request.GET.get('next') or request.POST.get('next')
#                 if next_url:
#                     return redirect(next_url)
                    
#                 return redirect('accounts:dashboard')
#             else:
#                 messages.error(request, "Account not active. Please verify your email.")
#                 return redirect('accounts:login')
#         else:
#             messages.error(request, "Invalid email or password")
#             return redirect('accounts:login')

#     return render(request, 'accounts/login.html')


# @login_required(login_url='accounts:login')
# def logout(request):
#     """User logout view"""
#     auth.logout(request)
#     messages.success(request, "You have been logged out successfully")
#     return redirect('accounts:login')


# def activate(request, uidb64, token):
#     """Account activation view"""
#     try:
#         uid = urlsafe_base64_decode(uidb64).decode()
#         user = Account.objects.get(pk=uid)
#     except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
#         user = None

#     if user is not None and default_token_generator.check_token(user, token):
#         user.is_active = True
#         user.save()
#         # Ensure user profile exists
#         UserProfile.objects.get_or_create(user=user)
#         messages.success(request, 'Your account has been activated successfully!')
#         return redirect('accounts:login')
#     else:
#         messages.error(request, 'Invalid activation link')
#         return redirect('accounts:register')


# # ====================== PROFILE VIEWS ====================== 
# @login_required(login_url='accounts:login')
# def dashboard(request):
#     """User dashboard view with order stats and referrals"""
#     try:
#         # Get user orders
#         orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')[:10]
#         orders_count = Order.objects.filter(user=request.user, is_ordered=True).count()
        
#         # Get or create user profile
#         userprofile, created = UserProfile.objects.get_or_create(user=request.user)
        
#         # Get referred users
#         referred_users = Account.objects.filter(referred_by=request.user)
        
#         # Generate referral link
#         referral_link = request.build_absolute_uri(
#             reverse('accounts:register') + f"?ref={request.user.referral_code}"
#         ) if hasattr(request.user, 'referral_code') and request.user.referral_code else ""
        
#         context = {
#             'orders': orders,
#             'orders_count': orders_count,
#             'userprofile': userprofile,
#             'referral_link': referral_link,
#             'referred_users': referred_users,
#         }
#         return render(request, 'accounts/dashboard.html', context)
        
#     except Exception as e:
#         messages.error(request, f'Dashboard error: {str(e)}')
#         return redirect('store')


# @login_required(login_url='accounts:login')
# def edit_profile(request):
#     """Edit user profile view"""
#     try:
#         userprofile, created = UserProfile.objects.get_or_create(user=request.user)
        
#         if request.method == 'POST':
#             user_form = UserForm(request.POST, instance=request.user)
#             profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)

#             if user_form.is_valid() and profile_form.is_valid():
#                 user_form.save()
#                 profile_form.save()
#                 messages.success(request, 'Your profile has been updated successfully!')
#                 return redirect('accounts:edit_profile')
#             else:
#                 messages.error(request, 'Please correct the errors below.')
#         else:
#             user_form = UserForm(instance=request.user)
#             profile_form = UserProfileForm(instance=userprofile)

#         context = {
#             'user_form': user_form,
#             'profile_form': profile_form,
#             'userprofile': userprofile,
#         }
#         return render(request, 'accounts/edit_profile.html', context)
        
#     except Exception as e:
#         messages.error(request, f'Profile error: {str(e)}')
#         return redirect('accounts:dashboard')


# @login_required(login_url='accounts:login')
# def change_password(request):
#     """Change user password view"""
#     if request.method == 'POST':
#         current_password = request.POST.get('current_password', '').strip()
#         new_password = request.POST.get('new_password', '').strip()
#         confirm_password = request.POST.get('confirm_password', '').strip()

#         # Validation
#         if not all([current_password, new_password, confirm_password]):
#             messages.error(request, 'All fields are required')
#             return redirect('accounts:change_password')

#         if len(new_password) < 8:
#             messages.error(request, 'Password must be at least 8 characters long')
#             return redirect('accounts:change_password')

#         if new_password != confirm_password:
#             messages.error(request, 'New passwords do not match')
#             return redirect('accounts:change_password')

#         # Check current password and update
#         user = request.user
#         if user.check_password(current_password):
#             user.set_password(new_password)
#             user.save()
#             update_session_auth_hash(request, user)  # Keep user logged in
#             messages.success(request, 'Password updated successfully!')
#             return redirect('accounts:dashboard')
#         else:
#             messages.error(request, 'Current password is incorrect')
#             return redirect('accounts:change_password')

#     return render(request, 'accounts/change_password.html')


# # ====================== PASSWORD RESET VIEWS ====================== 
# def forgotPassword(request):
#     """Forgot password view"""
#     if request.method == 'POST':
#         email = request.POST.get('email', '').strip()
        
#         if not email:
#             messages.error(request, 'Email address is required')
#             return redirect('accounts:forgotPassword')

#         try:
#             user = Account.objects.get(email__iexact=email)
            
#             # Send password reset email
#             current_site = get_current_site(request)
#             mail_subject = 'Reset Your Password'
#             message = render_to_string('accounts/reset_password_email.html', {
#                 'user': user,
#                 'domain': current_site.domain,
#                 'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#                 'token': default_token_generator.make_token(user),
#             })
            
#             EmailMessage(mail_subject, message, to=[email]).send()
#             messages.success(request, 'Password reset email has been sent to your email address.')
#             return redirect('accounts:login')
            
#         except Account.DoesNotExist:
#             messages.error(request, 'Account with this email address does not exist.')
#             return redirect('accounts:forgotPassword')

#     return render(request, 'accounts/forgotPassword.html')


# def resetpassword_validate(request, uidb64, token):
#     """Validate password reset link"""
#     try:
#         uid = urlsafe_base64_decode(uidb64).decode()
#         user = Account.objects.get(pk=uid)
#     except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
#         user = None

#     if user is not None and default_token_generator.check_token(user, token):
#         request.session['uid'] = uid
#         messages.success(request, 'Please reset your password')
#         return redirect('accounts:resetPassword')
#     else:
#         messages.error(request, 'This link has expired!')
#         return redirect('accounts:login')


# def resetPassword(request):
#     """Reset password view"""
#     if request.method == 'POST':
#         password = request.POST.get('password', '').strip()
#         confirm_password = request.POST.get('confirm_password', '').strip()

#         # Validation
#         if not password or not confirm_password:
#             messages.error(request, 'Both password fields are required')
#             return redirect('accounts:resetPassword')

#         if len(password) < 8:
#             messages.error(request, 'Password must be at least 8 characters long')
#             return redirect('accounts:resetPassword')

#         if password != confirm_password:
#             messages.error(request, 'Passwords do not match')
#             return redirect('accounts:resetPassword')

#         # Reset password
#         uid = request.session.get('uid')
#         if uid:
#             try:
#                 user = Account.objects.get(pk=uid)
#                 user.set_password(password)
#                 user.save()
#                 request.session.pop('uid', None)
#                 messages.success(request, 'Password reset successful')
#                 return redirect('accounts:login')
#             except Account.DoesNotExist:
#                 messages.error(request, 'Invalid session')
#                 return redirect('accounts:forgotPassword')
#         else:
#             messages.error(request, 'Session has expired')
#             return redirect('accounts:forgotPassword')

#     else:
#         # Check if session is valid
#         if not request.session.get('uid'):
#             messages.error(request, 'Session has expired')
#             return redirect('accounts:forgotPassword')

#         return render(request, 'accounts/resetPassword.html')


# # ====================== ORDER VIEWS ====================== 
# @login_required(login_url='accounts:login')
# def my_orders(request):
#     """Display user orders"""
#     orders = Order.objects.filter(
#         user=request.user, 
#         is_ordered=True
#     ).order_by('-created_at')
    
#     context = {
#         'orders': orders
#     }
#     return render(request, 'accounts/my_orders.html', context)


# @login_required(login_url='accounts:login')
# def order_detail(request, order_id):
#     """Display order details"""
#     try:
#         order = Order.objects.get(
#             order_number=order_id, 
#             user=request.user, 
#             is_ordered=True
#         )
#         ordered_products = OrderProduct.objects.filter(order=order)
        
#         subtotal = sum(item.product_price * item.quantity for item in ordered_products)
        
#         context = {
#             'order': order,
#             'ordered_products': ordered_products,
#             'subtotal': subtotal,
#         }
#         return render(request, 'accounts/order_detail.html', context)
        
#     except Order.DoesNotExist:
#         messages.error(request, 'Order not found')
#         return redirect('accounts:my_orders')


# @login_required(login_url='accounts:login')
# @csrf_exempt
# def delete_account(request):
#     """Deactivate user account"""
#     if request.method == 'POST':
#         password = request.POST.get('password', '').strip()
        
#         if not password:
#             messages.error(request, 'Password is required to deactivate account')
#             return redirect('accounts:dashboard')
        
#         if request.user.check_password(password):
#             request.user.is_active = False
#             request.user.save()
#             auth.logout(request)
#             messages.success(request, 'Your account has been deactivated successfully')
#             return redirect('store')
#         else:
#             messages.error(request, 'Incorrect password')
#             return redirect('accounts:dashboard')
            
#     return redirect('accounts:dashboard')


# # ====================== PAYMENT VIEWS ====================== 
# @login_required(login_url='accounts:login')
# def payments(request):
#     """Payment page view"""
#     order_number = request.session.get('order_number')
#     if not order_number:
#         messages.error(request, 'No active order found')
#         return redirect('carts:checkout')

#     try:
#         order = Order.objects.filter(
#             order_number=order_number,
#             is_ordered=False,
#             user=request.user
#         ).latest('created_at')
        
#         # Calculate amount in paise (Razorpay requires amount in smallest currency unit)
#         amount = int((order.order_total + order.tax) * 100)
        
#         # Create Razorpay order
#         client = get_razorpay_client()
#         razorpay_order = client.order.create({
#             'amount': amount,
#             'currency': 'INR',
#             'payment_capture': 1
#         })
        
#         # Save Razorpay order ID
#         order.razorpay_order_id = razorpay_order['id']
#         order.save()
        
#         context = {
#             'order': order,
#             'razorpay_key_id': getattr(settings, 'RAZORPAY_KEY_ID', ''),
#             'razorpay_order_id': razorpay_order['id'],
#             'amount': amount,
#             'callback_url': request.build_absolute_uri(reverse('accounts:payment_complete')),
#         }
#         return render(request, 'accounts/payments.html', context)
        
#     except Order.DoesNotExist:
#         messages.error(request, 'Order not found')
#         return redirect('carts:checkout')
#     except Exception as e:
#         messages.error(request, f'Payment setup failed: {str(e)}')
#         return redirect('carts:checkout')


# @login_required(login_url='accounts:login')
# @transaction.atomic
# def place_order(request):
#     """Place order and redirect to payment"""
#     if request.method == 'POST':
#         cart_items = CartItem.objects.filter(user=request.user)
#         if not cart_items.exists():
#             messages.error(request, 'Your cart is empty')
#             return redirect('store')

#         try:
#             # Generate unique order number
#             order_number = f"{datetime.now().strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:6]}"
            
#             # Calculate totals
#             subtotal = sum(item.product.price * item.quantity for item in cart_items)
#             tax = round(subtotal * 0.18, 2)  # 18% GST
            
#             # Create order
#             order = Order.objects.create(
#                 user=request.user,
#                 order_number=order_number,
#                 order_total=subtotal,
#                 tax=tax,
#             )
            
#             # Store order number in session
#             request.session['order_number'] = order.order_number
            
#             return redirect('accounts:payments')
            
#         except Exception as e:
#             messages.error(request, f'Failed to place order: {str(e)}')
#             return redirect('carts:checkout')
    
#     return redirect('carts:checkout')


# @csrf_exempt
# @transaction.atomic
# def payment_complete(request):
#     """Handle payment completion"""
#     if request.method == 'POST':
#         try:
#             # Get Razorpay response parameters
#             payment_id = request.POST.get('razorpay_payment_id')
#             razorpay_order_id = request.POST.get('razorpay_order_id')
#             signature = request.POST.get('razorpay_signature')
            
#             if not all([payment_id, razorpay_order_id, signature]):
#                 return HttpResponseBadRequest('Missing payment parameters')
            
#             # Verify payment signature
#             client = get_razorpay_client()
#             client.utility.verify_payment_signature({
#                 'razorpay_order_id': razorpay_order_id,
#                 'razorpay_payment_id': payment_id,
#                 'razorpay_signature': signature
#             })
            
#             # Get order
#             order = Order.objects.select_for_update().get(
#                 razorpay_order_id=razorpay_order_id,
#                 is_ordered=False,
#                 user=request.user
#             )
            
#             # Create payment record
#             payment = Payment.objects.create(
#                 user=request.user,
#                 payment_id=payment_id,
#                 payment_method='Razorpay',
#                 amount_paid=order.order_total + order.tax,
#                 status='Completed'
#             )
            
#             # Update order
#             order.payment = payment
#             order.is_ordered = True
#             order.save()
            
#             # Create order products from cart
#             cart_items = CartItem.objects.filter(user=request.user)
#             order_products = []
            
#             for item in cart_items:
#                 order_product = OrderProduct(
#                     order=order,
#                     payment=payment,
#                     user=request.user,
#                     product=item.product,
#                     quantity=item.quantity,
#                     product_price=item.product.price,
#                     ordered=True
#                 )
#                 order_products.append(order_product)
            
#             OrderProduct.objects.bulk_create(order_products)
            
#             # Clear cart
#             cart_items.delete()
            
#             # Send order confirmation email
#             try:
#                 current_site = get_current_site(request)
#                 mail_subject = 'Order Confirmation'
#                 message = render_to_string('accounts/order_confirmation_email.html', {
#                     'user': request.user,
#                     'order': order,
#                     'domain': current_site.domain,
#                 })
#                 EmailMessage(mail_subject, message, to=[request.user.email]).send()
#             except Exception:
#                 # Email sending failed, but continue with order completion
#                 pass
            
#             # Clean up session
#             request.session.pop('order_number', None)
            
#             return redirect('accounts:order_complete', 
#                           order_number=order.order_number, 
#                           payment_id=payment.payment_id)
            
#         except Order.DoesNotExist:
#             messages.error(request, 'Order not found')
#             return redirect('carts:checkout')
#         except Exception as e:
#             messages.error(request, f'Payment verification failed: {str(e)}')
#             return redirect('carts:checkout')
    
#     return HttpResponseBadRequest('Invalid request method')


# @login_required(login_url='accounts:login')
# def order_complete(request, order_number, payment_id):
#     """Order completion page"""
#     try:
#         order = Order.objects.get(
#             order_number=order_number,
#             is_ordered=True,
#             user=request.user
#         )
#         payment = Payment.objects.get(payment_id=payment_id, user=request.user)
#         ordered_products = OrderProduct.objects.filter(order=order)
        
#         subtotal = sum(item.product_price * item.quantity for item in ordered_products)
        
#         context = {
#             'order': order,
#             'payment': payment,
#             'ordered_products': ordered_products,
#             'subtotal': subtotal,
#         }
#         return render(request, 'accounts/order_complete.html', context)
        
#     except (Order.DoesNotExist, Payment.DoesNotExist):
#         messages.error(request, 'Order or payment information not found')
#         return redirect('store')


# # ====================== API VIEWS ====================== 
# @csrf_exempt
# def create_razorpay_order(request):
#     """API endpoint to create Razorpay order"""
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             amount_paise = int(float(data.get('amount', 0)) * 100)
            
#             if amount_paise <= 0:
#                 return JsonResponse({'error': 'Invalid amount'}, status=400)
                
#             client = get_razorpay_client()
#             rp_order = client.order.create({
#                 'amount': amount_paise,
#                 'currency': 'INR',
#                 'payment_capture': 1
#             })
            
#             return JsonResponse({
#                 'id': rp_order['id'],
#                 'currency': rp_order['currency'],
#                 'amount': rp_order['amount']
#             })
            
#         except json.JSONDecodeError:
#             return JsonResponse({'error': 'Invalid JSON data'}, status=400)
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=500)
            
#     return JsonResponse({'error': 'Method not allowed'}, status=405)





from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import update_session_auth_hash
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings
from django.db import transaction
from django.db.models import Count
from django.urls import reverse

import json
import razorpay
from datetime import datetime
import uuid

from .forms import RegistrationForm, UserForm, UserProfileForm
from .models import Account, UserProfile
from carts.models import Cart, CartItem
from carts.views import _cart_id
from orders.models import Order, OrderProduct, Payment


# -------------------- Razorpay Client Setup --------------------
def get_razorpay_client():
    """Initialize and return Razorpay client"""
    try:
        key = getattr(settings, "RAZORPAY_KEY_ID", None)
        secret = getattr(settings, "RAZORPAY_KEY_SECRET", None)

        if not key or not secret:
            raise ImproperlyConfigured("Razorpay keys are missing from settings")

        return razorpay.Client(auth=(key, secret))
    except Exception as e:
        raise ImproperlyConfigured(f"Error initializing Razorpay client: {str(e)}")


# ====================== AUTHENTICATION VIEWS ======================
# accounts/views.py

def register(request):
    """User registration view with referral system"""
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    first_name = form.cleaned_data['first_name']
                    last_name = form.cleaned_data['last_name']
                    phone_number = form.cleaned_data['phone_number']
                    email = form.cleaned_data['email']
                    password = form.cleaned_data['password']
                    username = email.split("@")[0]

                    # Create user
                    user = Account.objects.create_user(
                        first_name=first_name,
                        last_name=last_name,
                        email=email,
                        username=username,
                        password=password,
                    )
                    user.phone_number = phone_number

                    # ✅ AUTO-ACTIVATE USER (important line)
                    user.is_active = True

                    # Handle referral code
                    ref_code = form.cleaned_data.get('referral_code')
                    if ref_code:
                        try:
                            referring_user = Account.objects.get(referral_code=ref_code)
                            user.referred_by = referring_user
                        except Account.DoesNotExist:
                            messages.warning(request, 'Invalid referral code')

                    user.save()

                    # (Optional) you can keep or remove this email part
                    # If email config is not ready, it's okay to skip it
                    """
                    try:
                        current_site = get_current_site(request)
                        mail_subject = 'Activate your account'
                        message = render_to_string('accounts/account_verification_email.html', {
                            'user': user,
                            'domain': current_site.domain,
                            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                            'token': default_token_generator.make_token(user),
                        })
                        EmailMessage(mail_subject, message, to=[email]).send()
                        messages.success(request, 'Registration successful!')
                    except Exception as e:
                        messages.warning(request, 'Account created but verification email failed.')
                    """

                    messages.success(request, 'Registration successful! You can now log in.')
                    return redirect('accounts:login')

            except Exception as e:
                messages.error(request, f'Registration failed: {str(e)}')

    else:
        form = RegistrationForm()
        ref_code = request.GET.get('ref')
        if ref_code:
            form.fields['referral_code'].initial = ref_code

    return render(request, 'accounts/register.html', {'form': form})



def login(request):
    """User login view with cart merging"""
    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "").strip()

        if not email or not password:
            messages.error(request, "Please fill in both fields")
            return redirect("accounts:login")

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            if user.is_active:
                # Merge guest cart with user cart
                try:
                    guest_cart = Cart.objects.get(cart_id=_cart_id(request))
                    if CartItem.objects.filter(cart=guest_cart).exists():
                        guest_items = CartItem.objects.filter(cart=guest_cart)
                        user_items = CartItem.objects.filter(user=user)

                        guest_variations = [
                            list(item.variations.all()) for item in guest_items
                        ]
                        user_variations = [
                            list(item.variations.all()) for item in user_items
                        ]

                        for i, g_variation in enumerate(guest_variations):
                            if g_variation in user_variations:
                                index = user_variations.index(g_variation)
                                user_item = user_items[index]
                                user_item.quantity += guest_items[i].quantity
                                user_item.save()
                                guest_items[i].delete()
                            else:
                                guest_items[i].user = user
                                guest_items[i].save()
                except Exception:
                    # Cart merging failed, but continue with login
                    pass

                auth.login(request, user)
                messages.success(request, f"Welcome back, {user.first_name}!")

                next_url = request.GET.get("next") or request.POST.get("next")
                if next_url:
                    return redirect(next_url)

                return redirect("accounts:dashboard")
            else:
                messages.error(request, "Account not active. Please verify your email.")
                return redirect("accounts:login")
        else:
            messages.error(request, "Invalid email or password")
            return redirect("accounts:login")

    return render(request, "accounts/login.html")


@login_required(login_url="accounts:login")
def logout(request):
    """User logout view"""
    auth.logout(request)
    messages.success(request, "You have been logged out successfully")
    return redirect("accounts:login")


def activate(request, uidb64, token):
    """Account activation view"""
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        UserProfile.objects.get_or_create(user=user)
        messages.success(request, "Your account has been activated successfully!")
        return redirect("accounts:login")
    else:
        messages.error(request, "Invalid activation link")
        return redirect("accounts:register")


# ====================== PROFILE VIEWS ======================
@login_required(login_url="accounts:login")
def dashboard(request):
    """User dashboard view with order stats and referrals"""
    try:
        orders = Order.objects.filter(
            user=request.user, is_ordered=True
        ).order_by("-created_at")[:10]
        orders_count = Order.objects.filter(
            user=request.user, is_ordered=True
        ).count()

        userprofile, created = UserProfile.objects.get_or_create(user=request.user)

        referred_users = Account.objects.filter(referred_by=request.user)

        referral_link = (
            request.build_absolute_uri(
                reverse("accounts:register") + f"?ref={request.user.referral_code}"
            )
            if hasattr(request.user, "referral_code") and request.user.referral_code
            else ""
        )

        context = {
            "orders": orders,
            "orders_count": orders_count,
            "userprofile": userprofile,
            "referral_link": referral_link,
            "referred_users": referred_users,
        }
        return render(request, "accounts/dashboard.html", context)

    except Exception as e:
        messages.error(request, f"Dashboard error: {str(e)}")
        return redirect("store")


@login_required(login_url="accounts:login")
def edit_profile(request):
    """Edit user profile view"""
    try:
        userprofile, created = UserProfile.objects.get_or_create(user=request.user)

        if request.method == "POST":
            user_form = UserForm(request.POST, instance=request.user)
            profile_form = UserProfileForm(
                request.POST, request.FILES, instance=userprofile
            )

            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                messages.success(
                    request, "Your profile has been updated successfully!"
                )
                return redirect("accounts:edit_profile")
            else:
                messages.error(request, "Please correct the errors below.")
        else:
            user_form = UserForm(instance=request.user)
            profile_form = UserProfileForm(instance=userprofile)

        context = {
            "user_form": user_form,
            "profile_form": profile_form,
            "userprofile": userprofile,
        }
        return render(request, "accounts/edit_profile.html", context)

    except Exception as e:
        messages.error(request, f"Profile error: {str(e)}")
        return redirect("accounts:dashboard")


@login_required(login_url="accounts:login")
def change_password(request):
    """Change user password view"""
    if request.method == "POST":
        current_password = request.POST.get("current_password", "").strip()
        new_password = request.POST.get("new_password", "").strip()
        confirm_password = request.POST.get("confirm_password", "").strip()

        if not all([current_password, new_password, confirm_password]):
            messages.error(request, "All fields are required")
            return redirect("accounts:change_password")

        if len(new_password) < 8:
            messages.error(request, "Password must be at least 8 characters long")
            return redirect("accounts:change_password")

        if new_password != confirm_password:
            messages.error(request, "New passwords do not match")
            return redirect("accounts:change_password")

        user = request.user
        if user.check_password(current_password):
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Password updated successfully!")
            return redirect("accounts:dashboard")
        else:
            messages.error(request, "Current password is incorrect")
            return redirect("accounts:change_password")

    return render(request, "accounts/change_password.html")


# ====================== PASSWORD RESET VIEWS ======================
def forgotPassword(request):
    """Forgot password view"""
    if request.method == "POST":
        email = request.POST.get("email", "").strip()

        if not email:
            messages.error(request, "Email address is required")
            return redirect("accounts:forgotPassword")

        try:
            user = Account.objects.get(email__iexact=email)

            current_site = get_current_site(request)
            mail_subject = "Reset Your Password"
            message = render_to_string(
                "accounts/reset_password_email.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": default_token_generator.make_token(user),
                },
            )

            EmailMessage(mail_subject, message, to=[email]).send()
            messages.success(
                request,
                "Password reset email has been sent to your email address.",
            )
            return redirect("accounts:login")

        except Account.DoesNotExist:
            messages.error(request, "Account with this email address does not exist.")
            return redirect("accounts:forgotPassword")

    return render(request, "accounts/forgotPassword.html")


def resetpassword_validate(request, uidb64, token):
    """Validate password reset link"""
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session["uid"] = uid
        messages.success(request, "Please reset your password")
        return redirect("accounts:resetPassword")
    else:
        messages.error(request, "This link has expired!")
        return redirect("accounts:login")


def resetPassword(request):
    """Reset password view"""
    if request.method == "POST":
        password = request.POST.get("password", "").strip()
        confirm_password = request.POST.get("confirm_password", "").strip()

        if not password or not confirm_password:
            messages.error(request, "Both password fields are required")
            return redirect("accounts:resetPassword")

        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters long")
            return redirect("accounts:resetPassword")

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect("accounts:resetPassword")

        uid = request.session.get("uid")
        if uid:
            try:
                user = Account.objects.get(pk=uid)
                user.set_password(password)
                user.save()
                request.session.pop("uid", None)
                messages.success(request, "Password reset successful")
                return redirect("accounts:login")
            except Account.DoesNotExist:
                messages.error(request, "Invalid session")
                return redirect("accounts:forgotPassword")
        else:
            messages.error(request, "Session has expired")
            return redirect("accounts:forgotPassword")

    else:
        if not request.session.get("uid"):
            messages.error(request, "Session has expired")
            return redirect("accounts:forgotPassword")

        return render(request, "accounts/resetPassword.html")


# ====================== ORDER VIEWS ======================
@login_required(login_url="accounts:login")
def my_orders(request):
    """Display user orders"""
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by(
        "-created_at"
    )

    context = {"orders": orders}
    return render(request, "accounts/my_orders.html", context)


@login_required(login_url="accounts:login")
def order_detail(request, order_id):
    """Display order details"""
    try:
        order = Order.objects.get(
            order_number=order_id, user=request.user, is_ordered=True
        )
        ordered_products = OrderProduct.objects.filter(order=order)

        subtotal = sum(item.product_price * item.quantity for item in ordered_products)

        context = {
            "order": order,
            "ordered_products": ordered_products,
            "subtotal": subtotal,
        }
        return render(request, "accounts/order_detail.html", context)

    except Order.DoesNotExist:
        messages.error(request, "Order not found")
        return redirect("accounts:my_orders")


@login_required(login_url="accounts:login")
@csrf_exempt
def delete_account(request):
    """Deactivate user account"""
    if request.method == "POST":
        password = request.POST.get("password", "").strip()

        if not password:
            messages.error(request, "Password is required to deactivate account")
            return redirect("accounts:dashboard")

        if request.user.check_password(password):
            request.user.is_active = False
            request.user.save()
            auth.logout(request)
            messages.success(request, "Your account has been deactivated successfully")
            return redirect("store")
        else:
            messages.error(request, "Incorrect password")
            return redirect("accounts:dashboard")

    return redirect("accounts:dashboard")


# ====================== PAYMENT VIEWS ======================
@login_required(login_url="accounts:login")
def payments(request):
    """Payment page view"""
    order_number = request.session.get("order_number")
    if not order_number:
        messages.error(request, "No active order found")
        return redirect("carts:checkout")

    try:
        order = (
            Order.objects.filter(
                order_number=order_number, is_ordered=False, user=request.user
            )
            .order_by("-created_at")
            .latest("created_at")
        )

        amount = int((order.order_total + order.tax) * 100)

        client = get_razorpay_client()
        razorpay_order = client.order.create(
            {"amount": amount, "currency": "INR", "payment_capture": 1}
        )

        order.razorpay_order_id = razorpay_order["id"]
        order.save()

        context = {
            "order": order,
            "razorpay_key_id": getattr(settings, "RAZORPAY_KEY_ID", ""),
            "razorpay_order_id": razorpay_order["id"],
            "amount": amount,
            "callback_url": request.build_absolute_uri(
                reverse("accounts:payment_complete")
            ),
        }
        return render(request, "accounts/payments.html", context)

    except Order.DoesNotExist:
        messages.error(request, "Order not found")
        return redirect("carts:checkout")
    except Exception as e:
        messages.error(request, f"Payment setup failed: {str(e)}")
        return redirect("carts:checkout")


@login_required(login_url="accounts:login")
@transaction.atomic
def place_order(request):
    """Place order and redirect to payment"""
    if request.method == "POST":
        cart_items = CartItem.objects.filter(user=request.user)
        if not cart_items.exists():
            messages.error(request, "Your cart is empty")
            return redirect("store")

        try:
            order_number = f"{datetime.now().strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:6]}"

            subtotal = sum(item.product.price * item.quantity for item in cart_items)
            tax = round(subtotal * 0.18, 2)

            order = Order.objects.create(
                user=request.user,
                order_number=order_number,
                order_total=subtotal,
                tax=tax,
            )

            request.session["order_number"] = order.order_number

            return redirect("accounts:payments")

        except Exception as e:
            messages.error(request, f"Failed to place order: {str(e)}")
            return redirect("carts:checkout")

    return redirect("carts:checkout")


@csrf_exempt
@transaction.atomic
def payment_complete(request):
    """Handle payment completion"""
    if request.method == "POST":
        try:
            payment_id = request.POST.get("razorpay_payment_id")
            razorpay_order_id = request.POST.get("razorpay_order_id")
            signature = request.POST.get("razorpay_signature")

            if not all([payment_id, razorpay_order_id, signature]):
                return HttpResponseBadRequest("Missing payment parameters")

            client = get_razorpay_client()
            client.utility.verify_payment_signature(
                {
                    "razorpay_order_id": razorpay_order_id,
                    "razorpay_payment_id": payment_id,
                    "razorpay_signature": signature,
                }
            )

            order = Order.objects.select_for_update().get(
                razorpay_order_id=razorpay_order_id,
                is_ordered=False,
                user=request.user,
            )

            payment = Payment.objects.create(
                user=request.user,
                payment_id=payment_id,
                payment_method="Razorpay",
                amount_paid=order.order_total + order.tax,
                status="Completed",
            )

            order.payment = payment
            order.is_ordered = True
            order.save()

            cart_items = CartItem.objects.filter(user=request.user)
            order_products = []

            for item in cart_items:
                order_product = OrderProduct(
                    order=order,
                    payment=payment,
                    user=request.user,
                    product=item.product,
                    quantity=item.quantity,
                    product_price=item.product.price,
                    ordered=True,
                )
                order_products.append(order_product)

            OrderProduct.objects.bulk_create(order_products)

            cart_items.delete()

            try:
                current_site = get_current_site(request)
                mail_subject = "Order Confirmation"
                message = render_to_string(
                    "accounts/order_confirmation_email.html",
                    {
                        "user": request.user,
                        "order": order,
                        "domain": current_site.domain,
                    },
                )
                EmailMessage(mail_subject, message, to=[request.user.email]).send()
            except Exception:
                pass

            request.session.pop("order_number", None)

            return redirect(
                "accounts:order_complete",
                order_number=order.order_number,
                payment_id=payment.payment_id,
            )

        except Order.DoesNotExist:
            messages.error(request, "Order not found")
            return redirect("carts:checkout")
        except Exception as e:
            messages.error(request, f"Payment verification failed: {str(e)}")
            return redirect("carts:checkout")

    return HttpResponseBadRequest("Invalid request method")


@login_required(login_url="accounts:login")
def order_complete(request, order_number, payment_id):
    """Order completion page"""
    try:
        order = Order.objects.get(
            order_number=order_number, is_ordered=True, user=request.user
        )
        payment = Payment.objects.get(payment_id=payment_id, user=request.user)
        ordered_products = OrderProduct.objects.filter(order=order)

        subtotal = sum(item.product_price * item.quantity for item in ordered_products)

        context = {
            "order": order,
            "payment": payment,
            "ordered_products": ordered_products,
            "subtotal": subtotal,
        }
        return render(request, "accounts/order_complete.html", context)

    except (Order.DoesNotExist, Payment.DoesNotExist):
        messages.error(request, "Order or payment information not found")
        return redirect("store")


# ====================== API VIEWS ======================
@csrf_exempt
def create_razorpay_order(request):
    """API endpoint to create Razorpay order"""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            amount_paise = int(float(data.get("amount", 0)) * 100)

            if amount_paise <= 0:
                return JsonResponse({"error": "Invalid amount"}, status=400)

            client = get_razorpay_client()
            rp_order = client.order.create(
                {"amount": amount_paise, "currency": "INR", "payment_capture": 1}
            )

            return JsonResponse(
                {
                    "id": rp_order["id"],
                    "currency": rp_order["currency"],
                    "amount": rp_order["amount"],
                }
            )

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Method not allowed"}, status=405)
