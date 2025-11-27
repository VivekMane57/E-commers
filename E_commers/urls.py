# E_commers/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("admin/", admin.site.urls),

    # Home page
    path("", views.home, name="home"),

    # Apps
    path("accounts/", include("accounts.urls")),
    path("store/", include("store.urls")),
    path("cart/", include("carts.urls")),
    path("orders/", include("orders.urls")),
    path("realtime/", include("realtime.urls")),  # BuyTogether features
]

# ❗ Serve media files (product images) even when DEBUG = False (Render)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
