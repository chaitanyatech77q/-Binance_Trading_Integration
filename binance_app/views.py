from decimal import Decimal, InvalidOperation

import requests
from django.conf import settings
from django.shortcuts import render
from django.views import View
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import TradeInputForm


def fetch_current_price(symbol: str) -> Decimal:
	base_url = getattr(settings, "BINANCE_BASE_URL", "https://api.binance.com")
	url = f"{base_url}/api/v3/ticker/price"
	resp = requests.get(url, params={"symbol": symbol.upper()}, timeout=10)
	resp.raise_for_status()
	data = resp.json()
	return Decimal(data["price"])  # raises KeyError if malformed


def calculate_targets(current_price: Decimal, tp_percent: Decimal, sl_percent: Decimal) -> dict:
	tp_target = current_price + (current_price * tp_percent / Decimal("100"))
	sl_target = current_price - (current_price * sl_percent / Decimal("100"))
	return {
		"current_price": current_price,
		"tp_target": tp_target,
		"sl_target": sl_target,
	}


class IndexView(View):
	template_name = "binance_app/index.html"

	def get(self, request):
		form = TradeInputForm()
		return render(request, self.template_name, {"form": form})

	def post(self, request):
		form = TradeInputForm(request.POST)
		context = {"form": form, "result": None, "error": None}
		if form.is_valid():
			symbol = form.cleaned_data["symbol"].upper()
			try:
				current_price = fetch_current_price(symbol)
				tp_percent = Decimal(str(form.cleaned_data["tp_percent"]))
				sl_percent = Decimal(str(form.cleaned_data["sl_percent"]))
				result = calculate_targets(current_price, tp_percent, sl_percent)
				context["result"] = {
					"symbol": symbol,
					"current_price": f"{result['current_price']:.8f}",
					"tp_target": f"{result['tp_target']:.8f}",
					"sl_target": f"{result['sl_target']:.8f}",
				}
			except (requests.RequestException, KeyError, InvalidOperation) as exc:
				context["error"] = f"Failed to fetch price or calculate targets: {exc}"
		return render(request, self.template_name, context)


class TradeCalcView(APIView):
	def post(self, request):
		symbol = str(request.data.get("symbol", "")).upper().strip()
		try:
			tp_percent = Decimal(str(request.data.get("tp_percent", "0")))
			sl_percent = Decimal(str(request.data.get("sl_percent", "0")))
		except InvalidOperation:
			return Response({"detail": "Invalid percentage values."}, status=status.HTTP_400_BAD_REQUEST)

		if not symbol:
			return Response({"detail": "Symbol is required."}, status=status.HTTP_400_BAD_REQUEST)
		if tp_percent < 0 or sl_percent < 0:
			return Response({"detail": "Percentages must be non-negative."}, status=status.HTTP_400_BAD_REQUEST)

		try:
			current_price = fetch_current_price(symbol)
			result = calculate_targets(current_price, tp_percent, sl_percent)
			return Response(
				{
					"symbol": symbol,
					"current_price": float(result["current_price"]),
					"take_profit_target": float(result["tp_target"]),
					"stop_loss_target": float(result["sl_target"]),
				}
			)
		except requests.HTTPError as exc:
			return Response({"detail": f"Binance error: {exc}"}, status=status.HTTP_502_BAD_GATEWAY)
		except requests.RequestException as exc:
			return Response({"detail": f"Network error: {exc}"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)


