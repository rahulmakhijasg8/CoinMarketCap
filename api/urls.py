from django.urls import path, include
from .views import CoinMarketCap
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('start_scrapping/', csrf_exempt(CoinMarketCap.as_view()))
]