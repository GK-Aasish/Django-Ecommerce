from django.urls import path
from .views.main_views import home, product_detail
from .views.auth_views import signup_view,login_view

urlpatterns = [
    path('', home, name='home'),
    path('product-detail/', product_detail, name='product_detail'),
    path('signup/', signup_view, name='signup'), 
    path('login/', login_view, name='login'),
]