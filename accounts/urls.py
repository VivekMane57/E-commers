# from django.urls import path
# from . import views

# app_name = 'accounts'  # Namespace declaration

# urlpatterns = [
#     # ===== AUTHENTICATION =====
#     path('register/', views.register, name='register'),
#     path('login/', views.login, name='login'),
#     path('logout/', views.logout, name='logout'),
#     path('activate/<uidb64>/<token>/', views.activate, name='activate'),

#     # ===== DASHBOARD & PROFILE =====
#     path('dashboard/', views.dashboard, name='dashboard'),
#     path('edit_profile/', views.edit_profile, name='edit_profile'),
#     path('change_password/', views.change_password, name='change_password'),
#     path('delete_account/', views.delete_account, name='delete_account'),

#     # ===== PASSWORD RESET =====
#     path('forgotPassword/', views.forgotPassword, name='forgotPassword'),
#     path('resetpassword_validate/<uidb64>/<token>/', 
#          views.resetpassword_validate, name='resetpassword_validate'),
#     path('resetPassword/', views.resetPassword, name='resetPassword'),

#     # ===== ORDERS =====
#     path('my_orders/', views.my_orders, name='my_orders'),
#     path('order_detail/<str:order_id>/', views.order_detail, name='order_detail'),

#     # ===== PAYMENTS =====
#     path('payments/', views.payments, name='payments'),
#     path('place_order/', views.place_order, name='place_order'),
#     path('payment_complete/', views.payment_complete, name='payment_complete'),
#     path('order_complete/<str:order_number>/<str:payment_id>/', 
#          views.order_complete, name='order_complete'),

#     # ===== API =====
#     path('create_razorpay_order/', views.create_razorpay_order, 
#          name='create_razorpay_order'),
# ]





from django.urls import path
from . import views

app_name = "accounts"  # Namespace declaration

urlpatterns = [
    # ===== AUTHENTICATION =====
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("activate/<uidb64>/<token>/", views.activate, name="activate"),

    # ===== DASHBOARD & PROFILE =====
    path("dashboard/", views.dashboard, name="dashboard"),
    path("edit_profile/", views.edit_profile, name="edit_profile"),
    path("change_password/", views.change_password, name="change_password"),
    path("delete_account/", views.delete_account, name="delete_account"),

    # ===== PASSWORD RESET =====
    path("forgotPassword/", views.forgotPassword, name="forgotPassword"),
    path(
        "resetpassword_validate/<uidb64>/<token>/",
        views.resetpassword_validate,
        name="resetpassword_validate",
    ),
    path("resetPassword/", views.resetPassword, name="resetPassword"),

    # ===== ORDERS =====
    path("my_orders/", views.my_orders, name="my_orders"),
    path("order_detail/<str:order_id>/", views.order_detail, name="order_detail"),

    # ===== PAYMENTS =====
    path("payments/", views.payments, name="payments"),
    path("place_order/", views.place_order, name="place_order"),
    path("payment_complete/", views.payment_complete, name="payment_complete"),
    path(
        "order_complete/<str:order_number>/<str:payment_id>/",
        views.order_complete,
        name="order_complete",
    ),

    # ===== API =====
    path(
        "create_razorpay_order/",
        views.create_razorpay_order,
        name="create_razorpay_order",
    ),
]
