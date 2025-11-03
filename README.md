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
- This project does not require any API keys or authentication.
It uses Binance’s public REST endpoints (e.g., /api/v3/ticker/price) to fetch market data directly through the base URL:

https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT


Since only public market data is accessed, no private keys, secrets, or authentication tokens are used or stored in this project.

### Tech stack used
- **Python**: 3.10+
- **Django**: 4.x
- **Django REST Framework (DRF)**
- **HTTP client**: `requests`
- **Env management**: `python-dotenv`
- **Database**: SQLite (default Django config)
- **Templates/UI**: Django templates with custom HTML/CSS
- **Testing**: Django `TestCase`, `unittest.mock`
- **External API**: Binance REST API (`/api/v3/ticker/price`)
- **Runtime**: WSGI (Django `wsgi.py`)


