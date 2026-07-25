"""
generate_seed_history.py
-------------------------
NOTE: This script is only used to seed the repository with realistic
example data for portfolio purposes, since the live fetch script needs
outbound internet access (which this generates instead, for demo purposes,
using realistic recent exchange rate ranges).

In real use, this file is not needed — fetch_exchange_rates.py hitting the
live Frankfurter API is what populates data/exchange_rate_history.csv going
forward (see the scheduled GitHub Action).

Run: python generate_seed_history.py
Output: ./exchange_rate_history.csv
"""

import csv
import random
from datetime import datetime, timedelta, timezone

random.seed(7)

BASE_CURRENCY = "USD"
# Realistic approximate rate ranges per currency (mid-2026 ballpark) with
# small day-to-day random walk to simulate real market movement.
STARTING_RATES = {
    "ZAR": 17.85,
    "EUR": 0.92,
    "GBP": 0.79,
    "JPY": 148.50,
    "AUD": 1.52,
}
VOLATILITY = {
    "ZAR": 0.12,
    "EUR": 0.004,
    "GBP": 0.003,
    "JPY": 0.6,
    "AUD": 0.006,
}

DAYS = 45
OUTPUT_FILE = "./exchange_rate_history.csv"

start_date = datetime.now(timezone.utc) - timedelta(days=DAYS)
rates = dict(STARTING_RATES)

rows = []
for day in range(DAYS):
    current_date = start_date + timedelta(days=day)
    # Skip weekends (FX markets are closed / API has no new data)
    if current_date.weekday() >= 5:
        continue
    date_str = current_date.strftime("%Y-%m-%d")
    fetched_at = current_date.strftime("%Y-%m-%d 06:00:00 UTC")

    for currency, vol in VOLATILITY.items():
        rates[currency] += random.uniform(-vol, vol)
        rows.append([fetched_at, date_str, BASE_CURRENCY, currency, round(rates[currency], 4)])

with open(OUTPUT_FILE, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["fetched_at", "rate_date", "base_currency", "target_currency", "rate"])
    writer.writerows(rows)

print(f"Seeded {len(rows)} rows across {DAYS} calendar days -> {OUTPUT_FILE}")
