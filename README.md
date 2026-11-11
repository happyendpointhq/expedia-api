# Expedia API and Scraper

The Expedia API returns travel data from Expedia as JSON: hotel and vacation rental search with
prices for your dates, hotel details, rooms and rates, photos, guest reviews, a price for every
check-in date and price insights, plus flights, rental cars, flight and hotel packages, activities
and destination guides, across Expedia's storefronts (US, UK, Germany, Canada, Australia and more).
It is a REST API, so you get Expedia data in your own code without writing and maintaining an
Expedia scraper.

Built and maintained by [Happy Endpoint](https://happyendpoint.com/library/expedia-api?utm_source=github&utm_medium=readme&utm_campaign=expedia-api).

- Subscribe and test every endpoint on RapidAPI: https://rapidapi.com/happyendpoint/api/expedia18
- Product page: https://happyendpoint.com/library/expedia-api?utm_source=github&utm_medium=readme&utm_campaign=expedia-api

---

## At a glance

| | |
|---|---|
| Base URL | `https://expedia18.p.rapidapi.com` |
| Auth | `x-rapidapi-key` and `x-rapidapi-host` headers |
| Endpoints | 38, all `GET` |
| Products | Hotels and vacation rentals, flights, cars, packages, activities, destinations |
| Markets | `market=us`, `uk`, `de`, `ca`, `au`, `fr`, `es`, `it` and the others `/markets` lists, each in its own currency |
| Page size | 50 hotels a page, up to 500 reachable per search |
| Format | JSON, every response wrapped in `{"success": true, "data": {...}}` |

---

## What data you get

**Hotels and vacation rentals**
- Search by destination, point and radius, map area, airport, a pasted Expedia URL, or price up to 50 hotels by id
- Total price with taxes and fees, nightly rate, strikethrough price, refundability, member deals, star class and guest score
- Details: description, address, amenities, check-in rules, fees, nearby places; every room type and rate for a stay
- Photos by category, guest reviews with replies, rating breakdowns, similar properties

**Prices over time**
- A hotel's lowest price for every check-in date, up to about 16 months ahead, in one call
- Whether a stay's price is low, typical or high; flight fare forecasts and the cheapest dates around a departure

**Flights, cars, packages and activities**
- One-way, round-trip and multi-city flights with segments, layovers and fare families
- Rental cars at airports and in cities, flight and hotel packages with the saving against booking separately
- Tours, tickets and day trips with bookable options and reviews

**Destinations**
- What a place is known for, the best months to visit with average hotel prices, things to do and travel tips

---

## Quick start

### 1. Get an API key

Subscribe on [RapidAPI](https://rapidapi.com/happyendpoint/api/expedia18). Current plans are listed there. Copy `.env.example` to `.env` and paste your key.

### 2. Make a request

Hotel searches take a `region_id` from `/locations`. Always send dates:

```bash
curl "https://expedia18.p.rapidapi.com/hotels/search?region_id=2621&check_in=2026-12-08&check_out=2026-12-11&adults=2&sort=price_low_to_high" \
  -H "x-rapidapi-host: expedia18.p.rapidapi.com" \
  -H "x-rapidapi-key: YOUR_RAPIDAPI_KEY"
```

### Python

```bash
pip install -r requirements.txt
cd examples/python
python quickstart.py "new york"
```

```python
from client import get

calendar = get("/hotels/price-calendar", hotel_id="17117062",
               start_date="2026-12-01", end_date="2027-02-28")
cheapest = min((d for d in calendar["days"] if d["price"]), key=lambda d: d["price"])
print(calendar["hotel"]["name"], cheapest["date"], cheapest["price_formatted"])
```

### JavaScript

```bash
RAPIDAPI_KEY=your_key node examples/javascript/quickstart.mjs "new york"
```

---

## Example response

`GET /hotels/search` for New York, 8 to 11 December 2026, one row, trimmed. More responses are in
[`samples/`](samples/).

```json
{
  "success": true,
  "data": {
    "market": "us",
    "currency": "USD",
    "check_in": "2026-12-08",
    "check_out": "2026-12-11",
    "nights": 3,
    "result_count": { "label": "300+ properties", "approximate": 300, "is_lower_bound": true },
    "hotels": [
      {
        "hotel_id": "19794327",
        "name": "31 Street Broadway Hotel",
        "star_rating": 2,
        "guest_rating": { "score": 5.4, "scale": 10, "review_count": 1274 },
        "price": {
          "currency": "USD",
          "total": 775.76,
          "total_formatted": "$776 total",
          "per_night": 65,
          "per_night_formatted": "$65 nightly",
          "basis_label": "for 3 nights",
          "taxes_note": "Total with taxes and fees"
        },
        "is_refundable": false,
        "is_sponsored": false
      }
    ]
  }
}
```

`per_night` is $65 but the three-night total is $775.76: the nightly rate is before taxes and
fees. See "Things to know" below.

---

## Endpoints

Base URL: `https://expedia18.p.rapidapi.com`

### Locations

| Endpoint | Returns |
|---|---|
| `GET /locations` | Cities, neighbourhoods, landmarks, airports and hotels by name, with the `region_id`, `hotel_id` or `airport_code` searches take |
| `GET /markets` | Every `market` value with its currency, language, website and product lines |

### Hotel search

| Endpoint | Returns |
|---|---|
| `GET /hotels/search` | Hotels in a destination for dates and guests, with sort and price, star, rating and cancellation filters |
| `GET /hotels/search-by-coordinates` | Hotels around a point |
| `GET /hotels/search-by-bounds` | Hotels inside a map rectangle |
| `GET /hotels/search-near-airport` | Hotels near an airport by IATA code |
| `GET /hotels/batch` | Prices for up to 50 hotels by id in one call |
| `GET /hotels/search-filters` | Every filter a destination offers, with the values to send |
| `GET /hotels/search-by-url` | The search a pasted Expedia search URL describes |

### Hotel details, prices and reviews

| Endpoint | Returns |
|---|---|
| `GET /hotels/details` | One hotel or rental: description, address, amenities, policies, fees, nearby places |
| `GET /hotels/details-by-url` | The same from a pasted Expedia hotel link |
| `GET /hotels/photos` | The full categorised photo gallery |
| `GET /hotels/rooms` | Every room type and rate for a stay, with taxes and cancellation terms |
| `GET /hotels/host` | The host profile of a vacation rental |
| `GET /hotels/similar` | Similar properties with rating and price |
| `GET /hotels/price-calendar` | The lowest price for every check-in date, up to about 16 months |
| `GET /hotels/price-insight` | Whether a stay's price is low, typical or high |
| `GET /hotels/reviews-summary` | Score, category scores, rating distribution and summary |
| `GET /hotels/reviews` | Guest reviews with replies and photos, sortable and searchable |

### Flights

| Endpoint | Returns |
|---|---|
| `GET /flights/search` | One-way flights or the outbound leg of a round trip, with segments and fare families |
| `GET /flights/search-return` | Return flights for a chosen outbound, priced as the round trip |
| `GET /flights/search-multi-city` | Multi-city trips of 2 to 5 flights |
| `GET /flights/search-filters` | Stops, airlines, airports and times a trip offers |
| `GET /flights/price-insight` | Lowest fare now, forecast and fare history for a route and date |
| `GET /flights/flexible-dates` | The lowest fare on each of 7 dates around a departure |

### Cars, packages and activities

| Endpoint | Returns |
|---|---|
| `GET /cars/search` | Rental cars at an airport or in a city for pick-up and drop-off times |
| `GET /cars/details` | One car offer: inclusions, policies, branch, price breakdown |
| `GET /packages/search` | Flight and hotel packages per traveller, with the saving |
| `GET /activities/search` | Tours, tickets, day trips and shows in a destination |
| `GET /activities/details` | One activity: inclusions, meeting point, rating, lead price |
| `GET /activities/offers` | Bookable options of an activity on a date |
| `GET /activities/reviews` | Traveller reviews of an activity |

### Destinations

| Endpoint | Returns |
|---|---|
| `GET /destinations/details` | What a destination is known for |
| `GET /destinations/best-time-to-visit` | Twelve months of weather with the average nightly hotel price |
| `GET /destinations/things-to-do` | Top places to see, in themed groups |
| `GET /destinations/travel-tips` | Tips on language, budget, getting around and customs |
| `GET /destinations/top` | About 150 curated top destinations with their `region_id` |
| `GET /status` | Service health |

---

## Things to know about the data

These come from running the examples on 4 November 2026 on the `us` market. They are the
mistakes that give wrong numbers rather than errors.

- **A city search reaches past the city.** Sorted cheapest first, all ten cheapest hotels for
  "New York" (region `2621`) on 4 to 7 December were in New Jersey, and 29 of the first 50.
  Check `address.region`, or search a neighbourhood `region_id` such as Manhattan.
- **`per_night` is before taxes and fees, `total` is not.** One Manhattan hotel showed $65
  nightly and $775.76 for three nights. Divide `total` by nights to compare hotels, as
  `client.nightly_with_taxes()` does.
- **Fees at the property sit in a list of sentences.** `fees.mandatory` mixes headings with
  charges; the PUBLIC hotel listed a $200 deposit and a $51.64 per night resort fee there.
- **Send dates.** Without `check_in` and `check_out`, prices are for a one-night stay Expedia
  picks, reported under `priced_for`.
- **Counts are labels.** `result_count` is `"300+ properties"` with `is_lower_bound: true`, and a
  search can be paged to 500 results at most.
- **Vacation rentals come back with hotels.** Rows with `unit_details` (`"Entire property by
  Vrbo"`) have no star rating. Filter them out for a hotel-only comparison.
- **Scores can rest on few reviews.** One property scored 9.6 from 5 reviews; new ones have
  none. Read `review_count` with `score`.
- **Ids are strings.** Some neighbourhood `region_id` values have 18 digits
  (`553248633938969338`). Do not cast them to numbers.
- **The price calendar is one night, recently seen.** `price_basis` is "Lowest prices in the past
  24 hours", and 5 of 120 dates came back with `price: null` and a sold-out note. At one Manhattan
  hotel the median check-in price was $615 in December and $341 in February, and Sunday check-ins
  were the cheapest ($303 median against $410 on Fridays).

---

## Examples in this repo

| File | What it does |
|---|---|
| [`examples/python/quickstart.py`](examples/python/quickstart.py) | Finds a city, lists the cheapest hotels for 3 nights 30 days out with the real nightly price, then opens the cheapest with its check-in rules and fees |
| [`examples/python/cheapest_dates.py`](examples/python/cheapest_dates.py) | The cheapest check-in dates at one hotel over the next months, with medians by month and weekday, from one price calendar call |
| [`examples/javascript/quickstart.mjs`](examples/javascript/quickstart.mjs) | The quickstart in Node 18+, no dependencies |
| [`samples/`](samples/) | Real responses from four endpoints |

---

## API or your own Expedia scraper

An Expedia scraper has to deal with bot protection, storefront differences and a search page
that changes often, and it tends to break on prices first. This API returns the same hotels,
rates, calendars and reviews as documented JSON on every storefront, so the work you keep is the
analysis. For a one-off export or a recurring price feed instead of API calls,
[contact us](https://happyendpoint.com/contact?utm_source=github&utm_medium=readme&utm_campaign=expedia-api).

---

## Use it from Claude, Cursor or any MCP client

RapidAPI exposes every endpoint as an MCP tool, so an AI assistant can search Expedia without
code:

```json
{
  "mcpServers": {
    "expedia": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "https://mcp.rapidapi.com",
        "--header",
        "x-api-host: expedia18.p.rapidapi.com",
        "--header",
        "x-api-key: YOUR_RAPIDAPI_KEY"
      ]
    }
  }
}
```

| Client | Config path |
|---|---|
| Claude Desktop (macOS) | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| Claude Desktop (Windows) | `%APPDATA%\Claude\claude_desktop_config.json` |
| Cursor | `~/.cursor/mcp.json` |
| Claude Code | `.mcp.json` in your project root |

---

## FAQ

### Is there an Expedia API?

Expedia's own APIs are for approved partners. This API, built and maintained by Happy Endpoint
and independent of Expedia, returns Expedia hotel, flight, car, package and activity data as
REST and JSON with a RapidAPI key.

### Can I get Expedia hotel prices for specific dates?

Yes. `/hotels/search` prices every hotel for your check-in, check-out and guests, and
`/hotels/rooms` gives every room type and rate for one hotel. `price.total` includes taxes and
fees.

### How do I find the cheapest dates to stay at a hotel?

`/hotels/price-calendar` returns the lowest price for every check-in date in one call.
[`cheapest_dates.py`](examples/python/cheapest_dates.py) turns it into the cheapest dates and
medians by month and weekday.

### Does it work for other countries?

Yes. Set `market` (for example `uk` or `de`) to search that storefront in its currency.
`/markets` lists every value.

### How do I use the Expedia API in Python?

Install `requests`, set `RAPIDAPI_KEY`, and call the endpoints with the two RapidAPI headers.
[`examples/python/client.py`](examples/python/client.py) is a short client with helpers for
dates, locations and prices.

### Can I book through this API?

No. The API is for search, prices and research. Bookings happen on Expedia.

### Is there a free Expedia API?

Plans, including what each one allows, are on the
[RapidAPI listing](https://rapidapi.com/happyendpoint/api/expedia18), where every endpoint can
also be tested in the browser.

---

## Related repos

- [awesome-alternative-data](https://github.com/happyendpointhq/awesome-alternative-data) - alternative data sources for investment research
- [awesome-ecommerce-data-apis](https://github.com/happyendpointhq/awesome-ecommerce-data-apis) - ecommerce and marketplace data APIs
- [rent-com-api](https://github.com/happyendpointhq/rent-com-api) - US rental listings and rent estimates from Rent.com
- [uae-real-estate-api](https://github.com/happyendpointhq/uae-real-estate-api) - asking versus paid prices in Dubai

---

## Disclaimer

Happy Endpoint is an independent provider. This project is **not affiliated
with, endorsed by, sponsored by, or connected to** any of the websites,
platforms, retailers, or marketplaces referenced here or reachable through the
underlying APIs.

All product names, brands, trademarks, and registered trademarks are the
property of their respective owners. Any reference to them is descriptive only,
to identify the subject matter of the data, and does not imply any association
or endorsement.

Users are responsible for ensuring their use of any data complies with
applicable laws and the terms of service of the relevant source.

---

## About Happy Endpoint

[Happy Endpoint](https://happyendpoint.com) builds and maintains real-time data
APIs for property portals, retailers, and marketplaces. All APIs are available on
RapidAPI with a free tier.

- Catalogue: [happyendpoint.com/library](https://happyendpoint.com/library)
- Datasets: [happyendpoint.com/datasets](https://happyendpoint.com/datasets)
- Documentation: [docs.happyendpoint.com](https://docs.happyendpoint.com)
- Contact: hello@happyendpoint.com

## Licence

MIT. See [LICENSE](LICENSE).
