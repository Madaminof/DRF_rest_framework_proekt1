from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import CategoryAPI,ProductSignsAPI,ProductDetailSignsAPI

urlpatterns =[
    path('category/',CategoryAPI.as_view(),name='category'),
    path('product/', ProductSignsAPI.as_view(),name='product'),
    path('product_detail/<int:pk>', ProductDetailSignsAPI.as_view(),name='product_detail')


]