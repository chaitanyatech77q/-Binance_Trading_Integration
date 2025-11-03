# Binance Trading Integration (Django)

A simple Django app that integrates with the Binance REST API to fetch current prices and calculate Take Profit / Stop Loss targets.

## Features
- HTML form to input symbol, TP% and SL%
- DRF API endpoint to return JSON
- Environment variables via `.env` (optional)
- Basic unit test for API

## Quickstart

### 1) Create venv and install
```bash
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
```

### 2) Run migrations and server
```bash
python manage.py migrate
python manage.py runserver
```

Open `http://127.0.0.1:8000/` for the form UI.

### API
- Endpoint: `POST /api/trade-calc/`
- Body (JSON):
```json
{ "symbol": "BTCUSDT", "tp_percent": 5, "sl_percent": 2 }
```
- Response (JSON):
```json
{
  "symbol": "BTCUSDT",
  "current_price": 27000.0,
  "take_profit_target": 28350.0,
  "stop_loss_target": 26460.0
}
```

## Environment Variables
Create a `.env` (optional):
```
DJANGO_SECRET_KEY=change-me
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=*
BINANCE_BASE_URL=https://api.binance.com
```

## Tests
```bash
python manage.py test
```

## Notes
- Price source: `GET /api/v3/ticker/price?symbol=SYMBOL` on Binance public API.
- No API key needed for current price.


