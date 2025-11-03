from django.urls import path

from .views import IndexView, TradeCalcView


urlpatterns = [
	path("", IndexView.as_view(), name="index"),
	path("api/trade-calc/", TradeCalcView.as_view(), name="trade-calc"),
]


