"""The cheapest check-in dates at one hotel over the next few months, from one call.

    python cheapest_dates.py --hotel-id 17117062 --days 120
    python cheapest_dates.py "public ian schrager new york"

/hotels/price-calendar returns the lowest one-night price for every check-in date (up to
about 16 months ahead). This prints the cheapest dates, the median price per month and per
weekday, and writes every day to a CSV. With a hotel name instead of an id, one /locations
call finds the id first.
"""

import argparse
import csv
from collections import defaultdict
from datetime import date, timedelta
from statistics import median

from client import get

parser = argparse.ArgumentParser()
parser.add_argument("hotel", nargs="?", help="a hotel name to look up, if no --hotel-id")
parser.add_argument("--hotel-id")
parser.add_argument("--days", type=int, default=120, help="check-in dates to cover")
parser.add_argument("--market", default="us")
parser.add_argument("--out", default="price_calendar.csv")
args = parser.parse_args()

hotel_id = args.hotel_id
if not hotel_id:
    rows = get("/locations", query=args.hotel or "public ian schrager", type="hotels", market=args.market)
    hotels = [r for r in rows["results"] if r.get("hotel_id")]
    if not hotels:
        raise SystemExit("No hotel matches that name; pass --hotel-id instead.")
    hotel_id = hotels[0]["hotel_id"]
    print(f"{hotels[0]['full_name']} -> hotel_id {hotel_id}")

start = date.today() + timedelta(days=1)
calendar = get(
    "/hotels/price-calendar",
    hotel_id=hotel_id,
    start_date=start.isoformat(),
    end_date=(start + timedelta(days=args.days - 1)).isoformat(),
    market=args.market,
)
days = calendar["days"]
priced = [d for d in days if d["price"] is not None]
print(f"{calendar['hotel']['name']}: {calendar['currency']}, {calendar['price_basis'].lower()}")
print(f"{len(priced)} of {len(days)} check-in dates priced; the rest are sold out or closed\n")
if not priced:
    raise SystemExit("No priced dates in this window.")

print("Cheapest check-in dates:")
for d in sorted(priced, key=lambda d: (d["price"], d["date"]))[:8]:
    print(f"  {d['date']} {date.fromisoformat(d['date']):%a}  {d['price_formatted']}")

by_month, by_weekday = defaultdict(list), defaultdict(list)
for d in priced:
    day = date.fromisoformat(d["date"])
    by_month[d["date"][:7]].append(d["price"])
    by_weekday[day.weekday()].append(d["price"])

print("\nMedian by month:")
for month, prices in sorted(by_month.items()):
    print(f"  {month}  {median(prices):>7,.0f}  (low {min(prices):,}, high {max(prices):,}, {len(prices)} days)")
print("\nMedian by check-in weekday:")
for weekday, prices in sorted(by_weekday.items()):
    print(f"  {date(2026, 1, 5 + weekday):%a}  {median(prices):>7,.0f}")

with open(args.out, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["date", "weekday", "price", "note"])
    for d in days:
        writer.writerow([d["date"], f"{date.fromisoformat(d['date']):%a}", d["price"], d.get("note") or ""])
print(f"\nEvery day: {args.out}. These are one-night prices; check /hotels/rooms for a real stay.")
