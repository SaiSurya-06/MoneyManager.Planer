import requests

ALPHA_VANTAGE_API_KEY = "YOUR_API_KEY"  # Put this in your .env for production

def fetch_stock_price(symbol):
    url = (
        f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}"
    )
    r = requests.get(url)
    data = r.json()
    try:
        return float(data["Global Quote"]["05. price"])
    except Exception:
        return None

def fetch_mf_price(symbol):
    # Alpha Vantage supports some MF NAVs, else use a placeholder or free Indian MF API
    # For now, attempt the same as stock.
    return fetch_stock_price(symbol)

from django.conf import settings
ALPHA_VANTAGE_API_KEY = getattr(settings, "ALPHA_VANTAGE_API_KEY", "YOUR_API_KEY")