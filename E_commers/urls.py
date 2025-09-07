from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Homepage
    path('', views.home, name='home'),
    
    # Apps
    path('accounts/', include('accounts.urls')),
    path('store/', include('store.urls')),
    path('cart/', include('carts.urls')),
    path('orders/', include('orders.urls')),
    path('realtime/', include('realtime.urls')),  # BuyTogether features
]

# Dev-only media
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)