from django.urls import path
from .views.main_views import home, product_detail

urlpatterns = [
    path('', home, name='home'),
    path('product-detail/', product_detail, name='product_detail')
]