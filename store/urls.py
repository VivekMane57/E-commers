from django.urls import path
from . import views

# No app_name needed since no namespace in main URLs
urlpatterns = [
    path('', views.store, name='store'),  # homepage
    path('category/<slug:category_slug>/', views.store, name='products_by_category'),
    path('category/<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),
    path('search/', views.search, name='search'),
    path('submit_review/<int:product_id>/', views.submit_review, name='submit_review'),
]