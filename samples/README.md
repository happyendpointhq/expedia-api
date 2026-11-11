# Sample responses

Real `200` responses from four Expedia API endpoints, taken on 4 November 2026 on the `us`
market. Long arrays are cut to their first three items (the price calendar to its first 40
days, the hotel's fee lists kept whole). Field names and values are otherwise unchanged. File
names follow the endpoint path, with `/` as `_`.

| File | Request |
|---|---|
| `locations.json` | `GET /locations?query=new york&type=hotels` |
| `hotels_search.json` | `GET /hotels/search?region_id=178293&check_in=2026-12-08&check_out=2026-12-11&adults=2&sort=price_low_to_high` |
| `hotels_details.json` | `GET /hotels/details?hotel_id=17117062` |
| `hotels_price-calendar.json` | `GET /hotels/price-calendar?hotel_id=17117062&start_date=2026-11-05&end_date=2027-02-28` |

`hotels_search.json` keeps three of the 50 rows: the cheapest hotel, a hotel whose total is far
above three times its `per_night` (taxes and fees), and a vacation rental, whose coordinates are rounded to three decimals because it is a
private home. They are useful for
writing parsers and tests before you subscribe. Prices change by the hour, so do not hard-code
these values.
