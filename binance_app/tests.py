from decimal import Decimal
from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse


class TradeCalcAPITest(TestCase):
	@patch("binance_app.views.fetch_current_price", return_value=Decimal("27000"))
	def test_trade_calc_success(self, _mock_price):
		url = reverse("trade-calc")
		payload = {"symbol": "BTCUSDT", "tp_percent": 5, "sl_percent": 2}
		resp = self.client.post(url, data=payload, content_type="application/json")
		self.assertEqual(resp.status_code, 200)
		data = resp.json()
		self.assertEqual(data["symbol"], "BTCUSDT")
		self.assertAlmostEqual(data["current_price"], 27000.0)
		self.assertAlmostEqual(data["take_profit_target"], 28350.0)
		self.assertAlmostEqual(data["stop_loss_target"], 26460.0)


