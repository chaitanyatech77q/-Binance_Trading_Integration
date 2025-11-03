from django import forms


class TradeInputForm(forms.Form):
	symbol = forms.CharField(
		label="Coin Pair",
		max_length=20,
		help_text="Example: BTCUSDT",
	)
	tp_percent = forms.DecimalField(label="Take Profit %", min_value=0, max_digits=6, decimal_places=2)
	sl_percent = forms.DecimalField(label="Stop Loss %", min_value=0, max_digits=6, decimal_places=2)


