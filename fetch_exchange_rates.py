"""
fetch_exchange_rates.py
------------------------
Fetches the latest currency exchange rates from the Frankfurter API
(https://frankfurter.dev) — a free, no-API-key-required public API backed
by the European Central Bank.

Each run appends a new row per tracked currency to a historical CSV,
building up a time series over time. Designed to be run manually or on
a schedule (see .github/workflows/daily_fetch.yml for automation).

Run: python fetch_exchange_rates.py
Output: appends to ./exchange_rate_history.csv
"""

import csv
import os
from datetime import datetime, timezone

import requests

BASE_CURRENCY = "USD"
TARGET_CURRENCIES = ["ZAR", "EUR", "GBP", "JPY", "AUD"]
API_URL = f"https://api.frankfurter.app/latest?from={BASE_CURRENCY}"
OUTPUT_FILE = "./exchange_rate_history.csv"


def fetch_rates() -> dict:
    """Call the Frankfurter API and return the rates dict."""
    response = requests.get(API_URL, timeout=10)
    response.raise_for_status()
    payload = response.json()
    return payload["rates"], payload["date"]


def append_to_history(rates: dict, api_date: str) -> None:
    """Append one row per target currency to the historical CSV."""
    file_exists = os.path.isfile(OUTPUT_FILE)
    fetched_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    with open(OUTPUT_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["fetched_at", "rate_date", "base_currency", "target_currency", "rate"])

        for currency in TARGET_CURRENCIES:
            if currency in rates:
                writer.writerow([fetched_at, api_date, BASE_CURRENCY, currency, rates[currency]])
            else:
                print(f"Warning: {currency} not found in API response, skipping.")


def main():
    print(f"Fetching rates for base currency {BASE_CURRENCY}...")
    rates, api_date = fetch_rates()
    append_to_history(rates, api_date)
    print(f"Appended {len(TARGET_CURRENCIES)} rows for {api_date} -> {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
