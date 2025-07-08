from django.urls import path
from .views import ProductPriceFetcher

urlpatterns = [
    path('api/fetch-prices/', ProductPriceFetcher.as_view(), name='fetch-prices'),
]
