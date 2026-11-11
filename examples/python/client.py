"""Minimal client for the Expedia API on RapidAPI.

Set RAPIDAPI_KEY in your environment (or in a .env file at the repo root).
"""

import os
from datetime import date, timedelta

import requests

HOST = "expedia18.p.rapidapi.com"


def _load_dotenv():
    """Read RAPIDAPI_KEY from a .env in the current folder or the repo root, if present."""
    root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
    for path in (".env", os.path.join(root, ".env")):
        if os.path.exists(path):
            for line in open(path, encoding="utf-8"):
                key, sep, value = line.strip().partition("=")
                if sep and value and not key.startswith("#"):
                    os.environ.setdefault(key.strip(), value.strip())


_load_dotenv()


def get(path, **params):
    """GET an endpoint and return the `data` object of the response."""
    key = os.environ.get("RAPIDAPI_KEY")
    if not key:
        raise SystemExit("Set RAPIDAPI_KEY first (see .env.example).")
    response = requests.get(
        f"https://{HOST}{path}",
        params={k: v for k, v in params.items() if v is not None},
        headers={"x-rapidapi-host": HOST, "x-rapidapi-key": key},
        timeout=90,
    )
    response.raise_for_status()
    body = response.json()
    if not body.get("success", True):
        raise RuntimeError(f"{path} failed: {body}")
    return body["data"]


def stay(days_ahead=30, nights=3):
    """(check_in, check_out) as ISO dates, a set number of days from today.

    Without dates, hotel searches price a one-night stay Expedia picks, so always send them.
    """
    check_in = date.today() + timedelta(days=days_ahead)
    return check_in.isoformat(), (check_in + timedelta(days=nights)).isoformat()


def find(query, kinds=("CITY", "MULTICITY", "NEIGHBORHOOD"), market="us"):
    """The first /locations row of one of the given types (best match first).

    Ids are strings and can be 18 digits long, so never cast them to int.
    """
    rows = get("/locations", query=query, type="hotels", market=market)["results"]
    for row in rows:
        if row["type"] in kinds:
            return row
    raise SystemExit(f"No {'/'.join(kinds)} location matches {query!r}")


def nightly_with_taxes(hotel, nights):
    """Total for the stay divided by nights. `per_night` is before taxes and fees, and on
    some hotels the gap is large, so compare totals, not per_night."""
    price = hotel.get("price") or {}
    return round(price["total"] / nights, 2) if price.get("total") else None
